from hilti_profis.Config import MasterModule

class Welds(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','Welds']
        submodules_list = [
        ]
        super().__init__(basefile, headerpath, submodules_list)