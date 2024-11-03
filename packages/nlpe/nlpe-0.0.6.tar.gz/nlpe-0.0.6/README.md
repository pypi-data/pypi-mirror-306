# NLPE
**N**ural **L**anguage **P**rocess **E**xperiments (NLPE) is a python package supporting you setup NLP experiments fastly.

Its mission is tio reduce the duplicate labors when we set up and NLP models or framework in current popular deep learning framework or methodology.

## Installation

### Install with Pip
```
pip install nlpe
```
### Install with Conda
```
conda install codedoc::nlpe
```
### Install with Docker
```
docker run -it codedocx/nlpe
```
### Install with Source
```
git clone https://github.com/codesedoc/nlpe.git
cd nlpe
pip install -e .
```

## Experiment
There are examples of conducting expeirments by using nlpe at **experiment** dir.
The **experiment/semantic_similarity** is an example to calculate semantic similarity of two texts by fine-tuned the uncased [BERT](https://huggingface.co/google-bert/bert-base-uncased) on [STSB](https://huggingface.co/datasets/nyu-mll/glue) dataset.
```
cd experiment/semantic_similarity
pip install -r requrements.txt
python main.py -t sematic_similarity -d glue -a bert --eval_strategy epoch --output_dir tmp_trainer
```
> **Version: 0.0.6**
> 
> **E-mail: gocodedoc@gmail.com** 
> 
