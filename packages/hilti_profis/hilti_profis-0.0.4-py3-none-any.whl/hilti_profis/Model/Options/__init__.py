from hilti_profis.Config import MasterModule

class Options(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','Options']
        submodules_list = []
        super().__init__(basefile, headerpath, submodules_list)