from pathlib import Path
from typing import List
from nlpe import DatasetProxy, Data, TextData, DatasetSplitCategory, Text, Language
import json

def test_pseudo_dataset():
    pseudo_dataset = {DatasetSplitCategory.TRAIN: ["tr1", "tr2", "tr3"], DatasetSplitCategory.VALIDATION: ["v1, v2"], DatasetSplitCategory.TEST: ["te1"]}
    proxy = DatasetProxy(
        glossary="pseudo_dataset",  
        dataset_type=list,
        load_dataset_call=lambda proxy_self, split: pseudo_dataset[split], 
        dump_dataset_call=lambda proxy_self, split: True, 
        raw_dir=Path("tmp", "raw_dir"))
    test_data = Data(dataset_proxy=proxy)
    all_datasets = test_data.load_dataset()
    assert len(all_datasets) == 3
    for s, d in zip(DatasetSplitCategory.all, all_datasets):
        assert id(pseudo_dataset[s]) == id(d)
        
    for s in DatasetSplitCategory.all:
        assert id(pseudo_dataset[s]) == id(proxy.load_dataset(s))
        
def test_pseudo_data_io():
    pseudo_dataset = {DatasetSplitCategory.TRAIN: ["tr1", "tr2", "tr3"], DatasetSplitCategory.VALIDATION: ["v1, v2"], DatasetSplitCategory.TEST: ["te1"]}
    pseduo_raw_file = lambda raw_dir: Path(raw_dir, "pseduo.json")
    pseduo_split_file = lambda split: Path("tmp", "pseduo", f"{split}.json")
    def load_dataset_call(proxy_self: DatasetProxy, split: DatasetSplitCategory, *args, **kwargs):
        raw_dir = proxy_self.raw_dir
        if not pseduo_split_file(split).exists():
            print(f"load {split} from raw file: {pseduo_raw_file(raw_dir)}")
            return json.loads(pseduo_raw_file(raw_dir).read_text())[split]
        else:
            print(f"load {split} from pseduo file: {pseduo_split_file(split)}")
            return json.loads(pseduo_split_file(split).read_text())
        
    def dump_dataset_call(proxy_self: DatasetProxy, split: DatasetSplitCategory, *args, **kwargs):
        print(f"dump {split} to pseduo file: {pseduo_split_file(split)}")
        pseduo_split_file(split).parent.mkdir(parents=True, exist_ok=True)
        pseduo_split_file(split).write_text(json.dumps(pseudo_dataset[split]))
        return True
    
    proxy = DatasetProxy(
        glossary="pseudo_dataset_io",  
        dataset_type=list,  
        download_raw_call= lambda raw_dir: pseduo_raw_file(raw_dir).write_text(json.dumps(pseudo_dataset, indent=4)), 
        load_dataset_call=load_dataset_call, 
        dump_dataset_call=dump_dataset_call, 
        raw_dir=Path("tmp", "raw_dir"))
    
    test_data = Data(dataset_proxy=proxy)
    all_datasets = test_data.load_dataset()
    assert len(all_datasets) == 3
    for s, d in zip(DatasetSplitCategory.all, all_datasets):
        assert pseudo_dataset[s] == d
        
    for s in DatasetSplitCategory.all:
        pseudo_dataset[s] == test_data[s]
    
    for s in DatasetSplitCategory.all:
        pseudo_dataset[s] == test_data[s]
    
    test_data.dump_dataset() 


def test_pseudo_text_data():
    pseudo_dataset = {DatasetSplitCategory.TRAIN: ["Hello World.", "How are You."], DatasetSplitCategory.VALIDATION: ["I am validataion."], DatasetSplitCategory.TEST: ["Nice to meet you!"]}
    proxy = DatasetProxy(
        glossary="pseudo_text_dataset",  
        dataset_type=list,
        load_dataset_call=lambda proxy_self, split: pseudo_dataset[split], 
        dump_dataset_call=lambda proxy_self, split: True, 
        raw_dir=Path("tmp", "raw_dir"))
    
    test_data = TextData(dataset_proxy=proxy, map_dataset_to_text_list=lambda dataset: [Text(s) for s in dataset])
    text_set = set(test_data.all_texts)
    assert len(text_set) == 4
    for s in DatasetSplitCategory.all:
        for string in pseudo_dataset[s]:
            assert string in text_set
    
    test_data.statistic_all_texts(tokenizor=str.split)
    assert test_data.max_length == 4
    assert test_data.min_length == 2
    