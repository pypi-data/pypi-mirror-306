from typing import Any, Callable, Union

from .utils.glossary import Glossary


class ProxyBase:
    def __init__(self, glossary: Union[str, Glossary]) -> None:
        if isinstance(glossary, str):
            glossary = Glossary(glossary)
            if not glossary.name.endswith("_proxy"):
                glossary = Glossary(glossary.name + "_proxy")
        assert isinstance(glossary, Glossary)
        self._glossary = glossary

        
    @property
    def glossary(self) -> Glossary:
        return self._glossary
    
