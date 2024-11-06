from hilti_profis.Config import MasterModule

class Points(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','AnchorLayout', 'AnchorLayoutPoints']
        submodules_list = []
        super().__init__(basefile, headerpath, submodules_list)