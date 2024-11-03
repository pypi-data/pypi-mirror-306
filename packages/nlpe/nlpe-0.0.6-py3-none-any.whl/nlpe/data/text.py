from abc import ABC, abstractmethod
from enum import StrEnum, auto
from typing import Any, Callable, List, Optional, Union
from ..utils import global_logger
from .data import Data


class Language(StrEnum):
    ENGLISH = auto()
    JAPANESE = auto()
    CHINESE = auto()


class Text(str):        
    def __init__(self, *args, language: Language = Language.ENGLISH, **kwargs) -> None:
        super().__init__()
        assert isinstance(language, Language)
        self._language = language
    
    def tokens(self, tokenizor: Callable, **kwargs) -> List[Any]:
        assert isinstance(tokenizor, Callable)
        return tokenizor(self)
    
    def embeddings(self, encoder: Callable, **kwargs) -> Union[Any, List[Any]]:
        assert isinstance(encoder, Callable)
        return encoder(self)   
    
    @property
    def language(self):
        return self._language
    
    @language.setter
    def language(self, value):
        assert isinstance(value, Language) or Language(value).value == value
        self._language = value 
        
         
class Sentence(Text):
    pass
    

class TextData(Data):
    def __init__(self, map_dataset_to_text_list: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(map_dataset_to_text_list, Callable)
        self._map_dataset_to_text_list = map_dataset_to_text_list
        self._max_length = None
        self._min_length = None

    @property
    def all_texts(self) -> List[Text]:
        result = []
        for ds in self.load_dataset():
            text_list = self._map_dataset_to_text_list(ds)
            assert isinstance(text_list, List)
            for t in text_list:
                assert isinstance(t, Text)
                result.append(t)
        return result
    
    def statistic_all_texts(self, tokenizor: Callable) -> List[int]:
        all_lengthes = [len(t.tokens(tokenizor)) for t in self.all_texts]
        self._min_length = min(all_lengthes)
        self._max_length = max(all_lengthes)
        return all_lengthes
       
    @property
    def min_length(self) -> Optional[int]:
        if self._min_length is None:
            logger = global_logger()
            logger.warning("Should not use min_length before statisticing the all datasets!")
        return self._min_length
    
    @property
    def max_length(self) -> Optional[int]:
        if self._max_length is None:
            logger = global_logger()
            logger.warning("Should not use min_length before statisticing the all datasets!")
        return self._max_length
    