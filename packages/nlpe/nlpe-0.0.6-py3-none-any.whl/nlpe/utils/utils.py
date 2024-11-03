import json
import os.path
import sys
from typing import Any, Callable, Dict, List, Optional, Iterable, Union


def class_name_chain(cls: type):
    supers = cls.__mro__
    names = [c.__name__ for c in supers]
    return '-->'.join(names)


def jsonable(obj: Any):
    if isinstance(obj, dict):
        result = dict()
        for k, v in obj.items():
            if type(k) not in (str, int, float, bool, None):
                k=str(k)
            result[k] = jsonable(v)
        return result
    else:
        result = obj
        try:
            json.dumps(obj)
        except:
            result = str(obj)
        return result


def map_item_wise(map_fun, container, item_identify):
    def _map(item):
        if item_identify(item):
            return map_fun(item)

        if isinstance(item, Iterable):
            result = []
            for i in item:
                result.append(_map(i))
            result = type(item)(result)
            return result
        else:
            raise ValueError

    return _map(container)


def search_arg(name) -> bool:
    name = f'--{name}'
    args = sys.argv
    if name in args:
        return True
    return False


def set_up_args(args_file: str) -> None:
    assert os.path.isfile(args_file)
    with open(args_file) as af:
        args_dict: dict = json.load(af)
    flags = []
    for f in set(args_dict.get('flags', [])):
        if not search_arg(f):
            flags.append(f)
    for name, value in args_dict.items():
        if not search_arg(name):
            sys.argv.extend([f'--{name}', value])
    sys.argv.extend(map(lambda x: f'--{x}', flags))
    pass


def normalize_str_arg(arg: str):
    assert isinstance(arg, str)
    return arg.strip()