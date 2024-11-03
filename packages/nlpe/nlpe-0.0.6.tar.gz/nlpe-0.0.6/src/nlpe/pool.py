import uuid
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from typing import Any, Dict, List, Optional, Set, Union
from uuid import uuid4 as random_uuid, UUID


class PoolState(Enum):
    FREE = auto()
    BUSY = auto()
    EMPTY = auto()
    FULL = auto()


class TokenStatus(StrEnum):
    VALID = auto()
    INVALID = auto()


class UnifiedToken:
    def __init__(self, factor = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if factor is None:
            factor = random_uuid()
        self._factor = factor
        self._status = TokenStatus.VALID
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        assert isinstance(value, TokenStatus)
        self._status = value

    @property
    def factor(self):
        return self._factor

    def __eq__(self, value: object) -> bool:
        assert isinstance(value, UnifiedToken)
        return self.factor == value.factor
    
    def __hash__(self):
        return hash(self.factor)
    
    def __str__(self) -> str:
        return str(self.factor)
    
    def __repr__(self) -> str:
        return repr(self.factor)



POOL_DEFAULT_CAPACITY = 128


class Pool:
    def __init__(self, unit_type: type = object):
        self._state: PoolState = PoolState.FREE
        self._capacity: int = POOL_DEFAULT_CAPACITY
        assert isinstance(unit_type, type)
        self._unit_type = unit_type
        self._utoken2unit: Dict[UnifiedToken, self._unit_type] = dict()

    @property
    def size(self) -> int:
        return len(self._utoken2unit)
        
    @property
    def _all_units(self) -> List[Any]:
        return list(self._utoken2unit.values())
    
    def _new_unified_token(self, unit: Any) -> UnifiedToken:
        return UnifiedToken()

    def push(self, unit: Any) -> UnifiedToken:
        assert self.size < POOL_DEFAULT_CAPACITY
        assert isinstance(unit, self._unit_type)
        united_token = self._new_unified_token(unit)
        self._utoken2unit[united_token] = unit
        united_token.status = TokenStatus.VALID
        return united_token

    def pop(self, token: UnifiedToken, *args, **kwargs) -> Any:
        assert isinstance(token, UnifiedToken)
        assert token.status == TokenStatus.VALID
        result = self._utoken2unit.pop(token)
        token.status = TokenStatus.INVALID
        return result

    def search(self, token: UnifiedToken, *args, **kwargs) -> Optional[Any]:
        assert isinstance(token, UnifiedToken)      
        assert token.status == TokenStatus.VALID  
        result = self._utoken2unit.get(token, None)
        return result
    
    def reset(self) -> bool:
        for ut in self._utoken2unit:
            ut.status = TokenStatus.INVALID
        self._utoken2unit.clear()
        return True
