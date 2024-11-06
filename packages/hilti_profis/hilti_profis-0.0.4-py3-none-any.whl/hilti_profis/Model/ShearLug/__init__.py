from hilti_profis.Config import MasterModule

class ShearLug(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','ShearLug']
        submodules_list = []
        super().__init__(basefile, headerpath, submodules_list)