from copy import deepcopy
import sys
from argparse import ArgumentParser
from typing import Any, Callable
from nlpe import ArgumentFactory, ArgumentPool, Approach, EvaluatorProxy, Data, DatasetProxy, DatasetSplitCategory
from nlpe.utils import global_logger, Glossary
from nlpe.utils.test import extend_to_original_sys_argv

sys.argv.extend("-t simple_task -d simple_data -a simple_approach --debug --evaluator simple_evaluator".split())
print("Current sys.argv: ", sys.argv)

parser = ArgumentParser()
parser.add_argument("--evaluator", type=str)
arg_pool = ArgumentPool()
arg_pool.push(ArgumentFactory(process=lambda : vars(parser.parse_known_args[0]), argument_glossary=Glossary("my_argument"), argument_type=dict))

logger = global_logger()

class SimpleApproach(Approach):
    
    def _process(self, data: Data, evaluator_proxy: EvaluatorProxy, *args, **kwargs):
        logger.info(f"Processing dataset: {data.dataset_proxy.glossary}")
        logger.info(f"Dataset: {data.all_datasets}")
        
        data.load_dataset(DatasetSplitCategory.TRAIN)
        logger.info(f"Load Model")
        logger.info(f"Trainning")
        logger.info(f"Dump Model")
        
        data.load_dataset(DatasetSplitCategory.VALIDATION)
        logger.info(f"Evaluating")
        evaluation = evaluator_proxy.compute([1,2,3],[3,3,3])
        logger.info(f"Evaluation Result for Valid Set:")
        logger.info(evaluation)
        logger.info(f"Dump Evaluation Result for Valid Set")
        
        data.load_dataset(DatasetSplitCategory.TEST)
        logger.info(f'Testing')
        evaluation = evaluator_proxy.compute([1,2,4],[3,2,3])
        logger.info(f"Evaluation Result for Test Set:")
        logger.info(evaluation)
        logger.info(f"Dump Evaluation Result for Test Set")


def setup_function(function):
    extend_to_original_sys_argv("-t test_task -d test_data -a test_approach --debug")
    
def test_approach_pipeline():
    approach = SimpleApproach(glossary="simple_approach")
    dataset_proxy = DatasetProxy(glossary="simple_dataset_proxy", dataset_type=list, load_dataset_call=lambda *args, **kwargs: [1,2,3], dump_dataset_call=lambda *args, **kwargs: True)
    evaluator_proxy = EvaluatorProxy(glossary="simple_evaluator_proxy", compute_call=lambda pridiction, label: [*pridiction, *label])
    data = Data(dataset_proxy, evaluator_proxy)
    assert approach.processing_data is None
    approach.process(data, evaluator_proxy)
    assert approach.processing_data is None
