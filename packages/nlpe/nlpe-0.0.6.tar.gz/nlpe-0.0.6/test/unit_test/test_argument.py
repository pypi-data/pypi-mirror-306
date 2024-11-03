from copy import deepcopy
import dataclasses
from enum import Enum, StrEnum, auto
from pathlib import Path
import pytest
import sys
import argparse

# from nltk import EarleyChartParser
from nlpe import ArgumentPool, ArgumentFactory
from nlpe.utils.test import extend_to_original_sys_argv, extend_to_sys_argv

# import pip
# installed_packages = pip.get_installed_distributions()
# installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
#      for i in installed_packages])
# print(installed_packages_list)


def setup_function(function):
    extend_to_original_sys_argv("-t test_task -d test_dataset -a test_approach --debug")

def test_single_argument_pool():
    assert id(ArgumentPool()) ==  id(ArgumentPool())

    
def test_meta_argument():
    pool = ArgumentPool()
    pool.pop(pool.meta_argument_token)
    factory = pool.meta_argument_factory
    assert isinstance(pool.meta_argument, dict)
    assert isinstance(factory, ArgumentFactory)
    assert pool.meta_argument == factory.to_dict(factory.argument)
    assert pool.meta_argument["task"] == "test_task"
    assert pool.meta_argument["dataset"] == "test_dataset"
    assert pool.meta_argument["approach"] == "test_approach"
    current_size = pool.size
    pool.pop(pool.meta_argument_token)
    assert pool.size == current_size - 1
    pool.meta_argument
    assert pool.size == current_size
    # Path(pool.meta_argument["dataset_raw_dir"]).mkdir(parents=True, exist_ok=True)
    
    
def test_parse_argument():
    class test_enum(StrEnum):
        TEST = auto()
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--int_arg", type=int, required=True)
    parser.add_argument("--float_arg", type=float, required=True)
    parser.add_argument("--enum_arg", type=test_enum, required=True)
    
    
    extend_to_sys_argv("--int_arg 1 --float_arg 1.5 --enum_arg test")
    
    factory = ArgumentFactory(process = lambda : parser.parse_known_args()[0], argument_glossary="argparser", argument_type=argparse.Namespace, to_dict=vars)
    
    pool = ArgumentPool()
    current_size = pool.size
    token = pool.push(factory)
    assert factory.argument_type == argparse.Namespace
    assert isinstance(factory.argument, factory.argument_type)
    assert id(factory) == id(pool.search(token))
    factory = pool.search(token)
    assert factory.argument_dict["int_arg"] == 1
    assert factory.argument_dict["float_arg"] == 1.5
    assert factory.argument_dict["enum_arg"] == test_enum.TEST
    assert pool.size == current_size + 1