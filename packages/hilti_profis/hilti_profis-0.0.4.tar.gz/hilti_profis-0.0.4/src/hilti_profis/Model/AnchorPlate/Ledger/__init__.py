from hilti_profis.Config import MasterModule

class Ledger(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','AnchorPlate', 'LedgerAngleProfile']
        submodules_list = []
        super().__init__(basefile, headerpath, submodules_list)