from nlpe import Data, Approach


class PseduoApproach(Approach):
    def _process(self, data: Data, *args, **kwargs):
        pass
    
    
def test_pseduo_approach():
    approach = PseduoApproach(glossary="pseduo_approach")
    assert approach.processing_data == None
    assert approach.glossary.name == "pseduo_approach"