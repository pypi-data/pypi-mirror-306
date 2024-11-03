import argparse
import copy
import dataclasses
from functools import WRAPPER_ASSIGNMENTS, partial, update_wrapper, wraps
import json
import os
from pathlib import Path, PurePath
import sys
import uuid
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, fields, make_dataclass, Field, field
from enum import Enum, StrEnum, auto
from typing import Dict, Any, Set, Tuple, Union, Callable, Type, List, Optional, Iterable
from argparse import Namespace, ArgumentParser
from .utils import Glossary, GLOSSARY_POOL

from .utils import global_logger

from .pool import Pool, UnifiedToken
from .utils.design_patterns import singleton



class PATH_MODE(StrEnum):
    ABSTRACT = 'abs'
    RELATED = 'rel'

    def __str__(self):
        return self.value


def _parsing_meta_arg() -> Namespace:
    arg_parser = ArgumentParser(usage="Initialize Meta Arguments", add_help=False)
    arg_parser.add_argument("-t", "--task", help="Specify the name of task.", type=str, required=True)
    arg_parser.add_argument("-d", "--dataset", help="Specify the dataset need to be deal with.", type=str, required=True)
    arg_parser.add_argument("-a", "--approach", help="Specify the approach", type=str, required=True)
    arg_parser.add_argument("--path_mode", help="Specify the mode of path. 'abs': the abstract path; 'rel': the related path to the root dir", type=PATH_MODE, default=PATH_MODE.ABSTRACT, choices=[pm.value for pm in PATH_MODE])
    arg_parser.add_argument("--cache_dir", help="Specify the dir of cached files, the default is '.cache' refer to root dir", type=PurePath, default=PurePath(".cache"))
    arg_parser.add_argument("--dataset_raw_dir", help="Specify the dir of raw version of dataset", type=PurePath, default=None)
    arg_parser.add_argument("--force_cache", help="Whether or not force to download cached info, such as dataset, configuration, when cached file is exist.", action='store_true')
    arg_parser.add_argument("--debug", help="Whether or not execuate by debug mode", action='store_true')
    argument = arg_parser.parse_known_args()[0]
    if argument.dataset_raw_dir is None:
        argument.dataset_raw_dir = PurePath(argument.cache_dir, "dataset", argument.dataset, "raw")
    return argument

class ArgumentFactory:
    def __init__(self,
            process: Callable, 
            argument_glossary: Glossary, 
            argument_type: Type,
            to_dict: Callable = None,
            process_args: Optional[Union[List,Tuple]] = None, 
            process_kw_args: Optional[Dict[str, Any]] = None,
            ) -> None:
        if isinstance(argument_glossary, str):
            argument_glossary = Glossary(argument_glossary)
        assert isinstance(argument_glossary, Glossary)
        self._argument_glossary = argument_glossary
        assert isinstance(process, Callable)
        assert isinstance(argument_type, Type)
        self._argument_type = argument_type
        if process_args is not None:
            assert isinstance(process_args, List) or isinstance(process_args, Tuple)
        else:
            process_args = list()
        if process_kw_args is not None:
            assert isinstance(process_kw_args, Dict) or isinstance(process_kw_args, Dict)
        else:
            process_kw_args = dict()
        self._process = update_wrapper(partial(process, *process_args, **process_kw_args), process)
        if issubclass(argument_type, dict) and to_dict is None:
            to_dict = lambda a, *args, **kwargs: dict(deepcopy(a))
        assert isinstance(to_dict, Callable)
        self._to_dict = to_dict
        self._argument = None
        
    @property
    def argument_glossary(self) -> Callable:
        return self._argument_glossary
    
    @property
    def process(self) -> Callable:
        return self._process
    
    @property
    def argument_type(self):
        return self._argument_type
    
    @property
    def to_dict(self):
        return self._to_dict
    
    @property
    def argument_dict(self) -> Any:
        result = self.to_dict(self.argument)
        assert isinstance(result, Dict)
        return result
    
    @property
    def argument(self) -> Any:
        if self._argument is None:
            self._argument = self.process()
        assert isinstance(self._argument, self.argument_type)
        return self._argument
    

@singleton
class ArgumentPool(Pool):
    def __init__(self):
        super().__init__(unit_type=ArgumentFactory)
        self._meta_argument_token: UnifiedToken = None
        logger = global_logger()
        meta_argument = self.meta_argument
        if meta_argument["debug"]:
            logger.debug("*** Meta Arguments ***")
            for n, v in meta_argument.items():
                logger.debug(f"{n}: {v}")
    
    @property
    def all_args(self) -> Dict[Glossary, Dict[str, Any]]:
        result = dict()
        for u in self._all_units:
            result[u.argument_glossary]= u.argument_dict
        return result

    def __getitem__(self, item:Glossary) -> Optional[Any]:
        if isinstance(item, str):
            item = GLOSSARY_POOL.search(item)
        assert isinstance(item, Glossary)
        factory = self.search(UnifiedToken(factor=item))
        if factory:
            return factory.argument
        raise KeyError
    
    @property
    def meta_argument(self) -> Dict[str, Any]:
        factory = self.meta_argument_factory
        result = factory.argument_dict
        return result
    
    @property
    def meta_argument_factory(self) -> ArgumentFactory:
        factory = self.search(self.meta_argument_token)
        assert isinstance(factory, ArgumentFactory)
        return factory

    @property
    def meta_argument_token(self) -> UnifiedToken:
        if not isinstance(self._meta_argument_token, UnifiedToken):
            argument_glossary = Glossary("meta_argument", update=True)
            factory = ArgumentFactory(process=_parsing_meta_arg, argument_glossary=argument_glossary, argument_type=Namespace, to_dict=vars)
            self._meta_argument_token= self.push(factory)
        assert isinstance(self._meta_argument_token, UnifiedToken)
        return self._meta_argument_token
    
    def _new_unified_token(self, factory: ArgumentFactory) -> UnifiedToken:
        return UnifiedToken(factor=factory.argument_glossary)
    
    def push(self, factory: ArgumentFactory) -> UnifiedToken:
        return super().push(factory)
    
    def pop(self, token: UnifiedToken, *args, **kwargs) -> Any:
        result = super().pop(token, *args, **kwargs)
        self._meta_argument_token = None
        return result
    
    def search(self, token: UnifiedToken, *args, **kwargs) -> ArgumentFactory | None:
        return super().search(token, *args, **kwargs)
    
    def reset(self) -> bool:
        result = super().reset()
        self._meta_argument_token = None
        return result

        
