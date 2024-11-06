from hilti_profis.Config import MasterModule
from .Combos import Combos

class Loads(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','Loads']
        submodules_list = []
        self.Combos = Combos(basefile=basefile)
        super().__init__(basefile, headerpath, submodules_list)