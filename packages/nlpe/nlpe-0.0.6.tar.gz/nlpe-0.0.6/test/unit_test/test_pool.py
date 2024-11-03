from nlpe import Pool, POOL_DEFAULT_CAPACITY, UnifiedToken, TokenStatus

class MyUnit:
    pass

class MyPool(Pool):
    def __init__(self, unit_type: type = MyUnit):
        super().__init__(unit_type)
        
        

def test_basic():
    pool = MyPool()
    assert pool.size == 0
    assert POOL_DEFAULT_CAPACITY > 0
    assert isinstance(POOL_DEFAULT_CAPACITY, int)
    token2unit = dict()
    for i in range(POOL_DEFAULT_CAPACITY):
        assert pool.size == i
        unit = MyUnit()
        token2unit[pool.push(unit)] = unit
        assert pool.size == i + 1
    
    for t, u in token2unit.items():
        assert t.status == TokenStatus.VALID
        assert isinstance(pool.search(t), MyUnit)
        assert t.status == TokenStatus.VALID
        assert id(u) == id(pool.pop(t))
        assert t.status == TokenStatus.INVALID
    
    pool.push(unit)
    pool.push(unit)
    pool.push(unit)
    assert pool.size == 3
    assert pool.reset()
    assert pool.size == 0