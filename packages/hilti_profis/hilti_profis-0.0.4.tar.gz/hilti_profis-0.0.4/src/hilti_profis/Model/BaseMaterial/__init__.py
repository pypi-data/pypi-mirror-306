from hilti_profis.Config import MasterModule
from .SupplementaryRebar import SupplementaryRebar

class BaseMaterial(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','BaseMaterial']
        submodules_list = []
        self.SupplementaryRebar = SupplementaryRebar(basefile=basefile)
        super().__init__(basefile, headerpath, submodules_list)