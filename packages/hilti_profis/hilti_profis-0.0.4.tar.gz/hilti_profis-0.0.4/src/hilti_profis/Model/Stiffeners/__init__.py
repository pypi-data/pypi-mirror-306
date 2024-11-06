from hilti_profis.Config import MasterModule
from .Custom import Custom

class Stiffeners(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','Stiffeners']
        submodules_list = []
        self.Custom = Custom(basefile=basefile)
        super().__init__(basefile, headerpath, submodules_list)