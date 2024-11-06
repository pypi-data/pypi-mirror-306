from hilti_profis.Config import MasterModule

class Anchor(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','Anchor']
        submodules_list = []
        super().__init__(basefile, headerpath, submodules_list)