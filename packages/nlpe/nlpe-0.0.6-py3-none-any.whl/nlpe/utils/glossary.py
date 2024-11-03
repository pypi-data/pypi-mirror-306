
from enum import Enum
import re
from typing import Optional, Any, Self, Union, overload
from .utils import normalize_str_arg
from .log import global_logger
from .design_patterns import singleton
from ..pool import Pool, UnifiedToken


class Glossary(str):
    @overload
    def __new__(cls, name: Union[str, Self], /, **kwargs) -> Self: ...
        
    def __new__(cls, name: Union[str, Self], /, **kwargs) -> Self: 
        assert isinstance(name, str)
        return  str.__new__(cls, name)
        
    def __init__(self, name: Union[str, Self], /, abbreviation: str='', description:str='', update=False) -> None:
        if isinstance(name, Glossary):
            glossary = name
            name = glossary.name
            abbreviation = glossary.abbreviation
            description = glossary.description
            update = True
        else:
            name = normalize_str_arg(name)
            abbreviation = normalize_str_arg(abbreviation)
            description = normalize_str_arg(description)
            if not re.search('.', name):
                raise ValueError(f'"name" can not be empty')
            if not re.search('.', abbreviation):
                abbreviation = name
        self._name = name
        self._abbreviation=abbreviation
        self._description=description
        if GLOSSARY_POOL.search(self) and not update:
            logger = global_logger()
            logger.warning(f"({repr(self)}) has been exist!  A temprate glossary was initionlized without pushing it into GLOSSARY_POOL")
        else:
            GLOSSARY_POOL.push(self, force=update)

    uuid_type = str
    
    @property
    def name(self):
        return self._name
    
    @property
    def uuid(self):
        return self.name
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, desc: Optional[str]):
        if (desc is not None) and (not re.search('.', desc)):
                raise ValueError(f'Argument "desc" ({desc}) is invalid')
        self._description=desc
    
    @property
    def abbreviation(self) -> str:
        return self._abbreviation

    
    def __hash__(self) -> int:
        return hash(self.uuid)
    

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self.name==str(value)
        assert isinstance(value, Glossary)
        return self.uuid==value.uuid
    
    def __str__(self) -> str:
        return str(self.uuid)
    
    def __repr__(self) -> str:
        return f"Glossary ({self})"


class GlossaryEnum(Glossary, Enum):
    def _generate_next_value_(name, start, count, last_values) -> Glossary:
        return Glossary(name)


@singleton
class GlossaryPool(Pool):
    def __init__(self):
        super().__init__(unit_type=Glossary)
        
    def _new_unified_token(self, unit: Union[Any, Glossary]) -> UnifiedToken:
        if isinstance(unit, Glossary.uuid_type):
            return UnifiedToken(factor=unit)
        else:
            assert isinstance(unit, Glossary)
            return UnifiedToken(factor=unit.uuid)
    
    def reset(self):
        raise RuntimeError("Glossary Pool Can not be reseted")
    
    def pop(self, token: UnifiedToken, *args, **kwargs) -> Any:
        raise RuntimeError("Can not delete unit from Glossary Pool")
    
    def push(self, glossary: Glossary, force=False) -> UnifiedToken:
        old = self.search(glossary)
        if old:
            if not force:
                raise ValueError(f"({repr(old)}) has been exist! Overwrite the exsit glossary with current definiation by set 'force' to 'True'.")
            else:
                from .log import global_logger
                logger = global_logger()
                logger.warning(f"({repr(old)}) has been exist! Overwrite with ({repr(glossary)})")
        token = super().push(glossary)
        return token
    
    def search(self, glossary: Union[Any, Glossary], *args, **kwargs) -> Any | None:
        token = self._new_unified_token(glossary)
        return super().search(token, *args, **kwargs)
    
GLOSSARY_POOL = GlossaryPool()