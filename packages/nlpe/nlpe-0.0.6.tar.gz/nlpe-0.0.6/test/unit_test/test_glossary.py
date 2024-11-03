from enum import Enum, StrEnum, auto
from nlpe.utils import Glossary, GLOSSARY_POOL, GlossaryEnum

    
class NameEnum(GlossaryEnum):
    A = auto()
    
class NameStrEnum(StrEnum):
    A = auto()
    
def test_self():
    glossary = Glossary('glossary')
    assert isinstance(glossary, str)
    new_glossary = Glossary(glossary)
    assert new_glossary == glossary
    assert Glossary(Glossary('glossary', update=True)) == Glossary('glossary', update=True)
    
def test_enum():
    g = Glossary("A")
    GLOSSARY_POOL.search(g)
    print(repr(NameEnum(g).value))
    assert 1 != "A"
    assert NameStrEnum.A == "a"
    assert isinstance(NameStrEnum.A, NameStrEnum)
    assert isinstance(NameStrEnum.A, StrEnum)
    assert isinstance(NameStrEnum.A, str)
    assert isinstance(NameStrEnum("a"), NameStrEnum)
    assert isinstance(NameStrEnum("a"), str)
    assert NameEnum.A == g
    assert isinstance(NameEnum.A, NameEnum)
    assert isinstance(NameEnum.A, GlossaryEnum)
    assert isinstance(NameEnum.A, Glossary)
    assert isinstance(NameEnum(g).value, Glossary)
    assert isinstance(NameStrEnum.A, NameStrEnum)
    assert isinstance(NameEnum(g).value, str)
    assert NameEnum(g).value == "A"
    assert NameEnum(g).value == NameEnum(g).value
    