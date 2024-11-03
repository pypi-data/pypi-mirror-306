from abc import ABC, abstractmethod
from typing import Callable, Dict, Any, Union, Optional, List, Tuple, Iterable

from ..data import Data
from ..proxy import ProxyBase
from ..utils.utils import normalize_str_arg
from ..utils.glossary import Glossary
from ..argument import ArgumentPool


class Approach(ABC):
    def __init__(self, *args, glossary: Union[str, Glossary] = None, **kwargs):
        if glossary is None:
            glossary = ArgumentPool().meta_argument["approach"]
        if isinstance(glossary, str):
            glossary = Glossary(normalize_str_arg(glossary))
        assert isinstance(glossary, Glossary)
        self._glossary = glossary
        self._processing_data: Data = None


    @property
    def processing_data(self) -> Data:
        return self._processing_data
    
    @property
    def glossary(self) -> Glossary:
        return self._glossary

    @abstractmethod
    def _process(self, data: Data, *args, **kwargs):
        pass

    def process(self, data: Data, *args, **kwargs):
        assert isinstance(data, Data)
        self._processing_data = data
        self._process(data, *args, **kwargs)
        self._processing_data = None

