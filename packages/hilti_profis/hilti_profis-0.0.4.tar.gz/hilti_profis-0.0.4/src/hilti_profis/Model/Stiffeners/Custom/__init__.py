from hilti_profis.Config import MasterModule

class Custom(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','Stiffeners', 'CustomStiffenerSteelMaterial']
        submodules_list = []
        super().__init__(basefile, headerpath, submodules_list)