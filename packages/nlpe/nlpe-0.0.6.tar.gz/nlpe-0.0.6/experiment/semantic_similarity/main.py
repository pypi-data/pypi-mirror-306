import json
import os
from pathlib import Path
from nlpe import ArgumentPool, DatasetProxy, TextData, Text, DatasetSplitCategory, Approach, EvaluatorProxy, ArgumentFactory

os.environ["HF_HOME"] = str(Path(ArgumentPool().meta_argument["cache_dir"], "huggingface"))

from typing import Dict, List

from nlpe.utils import global_logger, jsonable
from transformers import BertForSequenceClassification, BertTokenizerFast
from transformers import Trainer, DataCollatorWithPadding, EvalPrediction, HfArgumentParser, TrainingArguments
from datasets import Dataset
from dataclasses import asdict
import torch
from functools import wraps
import random
from nlpe.utils.glossary import Glossary
import datasets
import evaluate
import numpy as np


class SigmoidClassifier(torch.nn.Linear):
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(super().forward(input))
    
class SementicSimilarity(Approach):
    def _process(self, data: TextData, *args, **kwargs):
        logger.info("Load tokenizer of BERT")
        tokenizer = BertTokenizerFast.from_pretrained("google-bert/bert-base-uncased", cache_dir=Path(meta_args["cache_dir"], "model"))
        data.statistic_all_texts(tokenizor=lambda text: tokenizer(text)["input_ids"])
        logger.info(f"Max lengtg of {data.dataset_name} is: {data.max_length}")
        logger.info(f"Min lengtg of {data.dataset_name} is: {data.min_length}")
        logger.info("Load pretraind BERT")
        model = BertForSequenceClassification.from_pretrained("google-bert/bert-base-uncased", cache_dir=Path(meta_args["cache_dir"], "model"), num_labels=1, problem_type = "regression")
        config = model.config
        model.classifier.forward = SigmoidClassifier(config.hidden_size, config.num_labels)
        assert config.num_labels == 1
        def tokenize_input(samples:Dict):
            inputs = tokenizer(samples["sentence1"], samples["sentence2"])
            if "label" in samples:
                inputs["label"] = samples["label"]
            return inputs
        
        logger.info("Initialize trainer")
        trainer = Trainer(
            model=model,
            args=ArgumentPool()["trainer_argument"],
            data_collator=DataCollatorWithPadding(tokenizer),
            train_dataset=stsb_data.load_dataset(DatasetSplitCategory.TRAIN).map(tokenize_input),
            eval_dataset=stsb_data.load_dataset(DatasetSplitCategory.VALIDATION).map(tokenize_input),
            compute_metrics=data.evaluator_proxy.compute
        )
        logger.info("Training")
        trainer.train()
        logger.info("Evaluation")
        logger.info(trainer.evaluate())
        logger.info("Testing")
        logger.info(trainer.evaluate(stsb_data.load_dataset(DatasetSplitCategory.TEST).map(tokenize_input), metric_key_prefix="test"))
    
    
def load_dataset_call(proxy: DatasetProxy, split: DatasetSplitCategory, *args, **kwargs):
    logger.info(f"Load STSB dataset, split: {split}")
    return datasets.load_dataset("nyu-mll/glue", name="stsb", split=split, cache_dir=Path(proxy.raw_dir))


def dump_dataset_call(proxy: DatasetProxy, split: DatasetSplitCategory, *args, **kwargs):
    dataset_dir = Path("dataset")
    dataset_dir.mkdir(exist_ok=True)
    dataset: datasets.Dataset = stsb_data.dataset[split]
    dataset.to_json(Path(dataset_dir, ArgumentPool().meta_argument["dataset"]),to_json_kwargs=dict(intent=4))


def evaluate(*args, **kwargs):
    import scipy.stats
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    # breakpoint()
    if len(args) == 0:
        predicts = kwargs["predicts"]
        labels = kwargs["labels"]
    elif len(args) == 1:
        eval_pre: EvalPrediction = args[0]
        assert isinstance(eval_pre, EvalPrediction)
        predicts = eval_pre.predictions
        labels = eval_pre.label_ids
    elif len(args) == 2:
        predicts, labels = args
    else:
        raise ValueError(f"{args} is not required")
    
    return {
        # "pearsonr_cor": scipy.stats.pearsonr(predicts, labels).pvalue,
        "pvalue": scipy.stats.spearmanr(predicts, labels).pvalue,
        "MAE": mean_absolute_error(predicts, labels),
        "MSE": mean_squared_error(predicts, labels)
    }
    
    
logger = global_logger()

# register the tranier arg to ArgumentPool
ArgumentPool().push(ArgumentFactory(
    argument_glossary="trainer_argument",
    argument_type= TrainingArguments,
    process=lambda : HfArgumentParser(TrainingArguments).parse_args_into_dataclasses(return_remaining_strings=True)[0], 
    to_dict=asdict))

logger.info("All arguments:")
logger.info(json.dumps(jsonable(ArgumentPool().all_args), indent=4))

# Synchronize random seed
seed = ArgumentPool()["trainer_argument"].seed
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)


# Prepare dataset
meta_args = ArgumentPool().meta_argument
dataset_proxy = DatasetProxy(
                             dataset_type=datasets.Dataset, 
                             load_dataset_call=load_dataset_call, 
                             dump_dataset_call=dump_dataset_call,
                             raw_dir=Path(meta_args["cache_dir"], "dataset"))
evaluator_Proxy = EvaluatorProxy(
    compute_call=evaluate
)
stsb_data = TextData(
    dataset_proxy=dataset_proxy, 
    map_dataset_to_text_list=lambda dataset: [Text(i) for i in dataset["sentence1"] + dataset["sentence2"]],
    evaluator_proxy= evaluator_Proxy)

# New approach
approach = SementicSimilarity()

# process data
approach.process(stsb_data)
