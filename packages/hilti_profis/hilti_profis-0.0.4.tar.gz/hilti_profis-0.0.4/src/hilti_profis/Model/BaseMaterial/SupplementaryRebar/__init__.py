from hilti_profis.Config import MasterModule

class SupplementaryRebar(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','BaseMaterial', 'SupplementaryReinforcement']
        submodules_list = []
        super().__init__(basefile, headerpath, submodules_list)