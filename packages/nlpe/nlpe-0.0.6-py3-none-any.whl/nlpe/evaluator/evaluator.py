from typing import Any, Callable

from ..utils.glossary import Glossary
from ..proxy import ProxyBase
from ..argument import ArgumentPool


class EvaluatorProxy(ProxyBase):
    def __init__(self, compute_call: Callable, glossary: Glossary=None) -> None:
        if glossary is None:
            glossary = ArgumentPool().meta_argument["dataset"] + "_evaluator"
        super().__init__(glossary)
        assert isinstance(compute_call, Callable)
        self._compute_call = compute_call
    
    def compute(self, *args, **kwargs) -> Any:
        return self._compute_call(*args, **kwargs)
