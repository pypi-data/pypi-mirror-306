import inspect
import os
from enum import StrEnum, auto
from pathlib import Path, PurePath
from typing import Optional, Tuple, Dict, Callable, Union, Any, List, Iterable

from ..argument import ArgumentPool, PATH_MODE
from ..utils import Glossary
from ..utils import singleton, global_logger, normalize_str_arg
from ..proxy import ProxyBase
from ..evaluator import EvaluatorProxy


class DatasetSplitCategory(StrEnum):
    TEST = 'test'
    TRAIN = 'train'
    VALIDATION = 'validation'

    @classmethod
    @property
    def all(cls):
        return tuple(DatasetSplitCategory)


class TaskCategory(StrEnum):
    CLASSIFICATION = 'classification'
    GENERATION = 'generation'
    REGRESSIVE = "regressive"


class DatasetProxy(ProxyBase):
    def __init__(self, dataset_type: type, load_dataset_call: Callable, dump_dataset_call: Callable, raw_dir:Path = None, download_raw_call: Optional[Callable] = None, glossary: Union[str, Glossary] = None) -> None:
        if glossary is None:
            glossary = ArgumentPool().meta_argument["dataset"]
        super().__init__(glossary=glossary)
        
        assert isinstance(dataset_type, type)
        self._dataset_type = dataset_type
        assert isinstance(load_dataset_call, Callable)
        self._load_dataset_call = load_dataset_call
        if dump_dataset_call is None:
            dump_dataset_call = lambda *args, **kwargs: True
        assert isinstance(dump_dataset_call, Callable)
        self._dump_dataset_call = dump_dataset_call
        
        if isinstance(raw_dir, str):
            raw_dir = Path(normalize_str_arg(raw_dir))
        assert raw_dir is None or isinstance(raw_dir, Path)
        if not isinstance(raw_dir, Path):
            meta_argument = ArgumentPool().meta_argument
            raw_dir= Path(meta_argument["dataset_raw_dir"])
        self._raw_dir = raw_dir
        
        if download_raw_call is None:
            download_raw_call = lambda *args, **kwargs: True
        assert isinstance(download_raw_call, Callable)
        self._download_raw_call = download_raw_call
        self.download_raw()
        
    @property
    def dataset_type(self):
        return self._dataset_type

    def download_raw(self, force=False):
        raw_dir = self.raw_dir
        logger = global_logger()
        if raw_dir.is_dir():
            if force:
                logger.warning(f"Redownload dataset raw to dir '{raw_dir}'!")
                for root, dirs, files in self.data_dir().walk(top_down = False, on_error=print):
                    for f in files:
                        Path(f).unlink()
                    for d in dirs:
                        Path(d).rmdir()
                assert len(raw_dir.iterdir()) == 0
        else:
            raw_dir.mkdir(parents=True)
        assert raw_dir.is_dir()
        assert self._download_raw_call(raw_dir)

    def load_dataset(self, split: DatasetSplitCategory, *args, **kwargs) -> Any:
        assert isinstance(split, DatasetSplitCategory)
        result = self._load_dataset_call(self, split, *args, **kwargs)
        assert isinstance(result, self._dataset_type)
        return result
    
    def dump_dataset(self, split: DatasetSplitCategory, *args, **kwargs) -> bool:
        assert isinstance(split, DatasetSplitCategory)
        return self._dump_dataset_call(self, split, *args, **kwargs)
    
    @property
    def raw_dir(self) -> Path: 
        return self._raw_dir
    
class Data:
    def __init__(self, dataset_proxy:DatasetProxy, evaluator_proxy:EvaluatorProxy = None):
        assert isinstance(dataset_proxy, DatasetProxy)
        self._dataset_proxy = dataset_proxy
        self._dataset: Dict[DatasetSplitCategory, Any] = None
        if evaluator_proxy is not None:
            assert isinstance(evaluator_proxy, EvaluatorProxy)
        self._evaluator_proxy = evaluator_proxy

    @property
    def dataset_proxy(self) -> DatasetProxy:
        return self._dataset_proxy
    
    @property
    def evaluator_proxy(self) -> EvaluatorProxy:
        return self._evaluator_proxy

    @property
    def dataset_name(self) -> str:
        return self._dataset_proxy.glossary.name
    
    @property
    def dataset_type(self):
        return self._dataset_proxy.dataset_type
    
    @property
    def all_datasets(self):
        return self.load_dataset()
    
    def __getitem__(self, key: DatasetSplitCategory):
        assert isinstance(key, DatasetSplitCategory)
        return self.load_dataset(key)
    
    def load_dataset(self, split: Union[DatasetSplitCategory, Tuple[DatasetSplitCategory]] = DatasetSplitCategory.all,  *args, **kwargs) -> Union[Any, Tuple[DatasetSplitCategory, Any]]:
        if isinstance(split, Tuple):
            result = []
            for s in split:
                assert isinstance(s, DatasetSplitCategory)
                result.append(self.load_dataset(s))
            result =  type(split)(result)

        elif isinstance(split, DatasetSplitCategory):
            if not isinstance(self._dataset, dict):
                self._dataset = dict()
            if split not in self._dataset:
                d = self._dataset_proxy.load_dataset(split)
                assert isinstance(d, self.dataset_type)
                self._dataset[split] = d
            result = self._dataset[split]
        elif split is None:
            result = None
        else:
            raise ValueError(f"Invaliad 'split': {split}")
        return result
    
    def dump_dataset(self, split: Union[DatasetSplitCategory, Tuple[DatasetSplitCategory]] = DatasetSplitCategory.all, *args, **kwargs) -> bool:
        result = True
        if isinstance(split, Tuple):
            for s in split:
                result = result and self.dump_dataset(s, *args, **kwargs)
        elif isinstance(split, DatasetSplitCategory):
            result = self._dataset_proxy.dump_dataset(split, *args, **kwargs)
        elif split is None:
            result = True
        else:
            raise ValueError(f"Invaliad 'split': {split}")
        return result
    
    
    def evaluate(self, *args, **kwargs):
        assert isinstance(self._evaluator_proxy, EvaluatorProxy)
        return self._evaluator_proxy.compute(*args, **kwargs)