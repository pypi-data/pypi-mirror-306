from hilti_profis.Config import MasterModule
from .AnchorPlate import AnchorPlate
from .AnchorLayout import AnchorLayout
from .Anchor import Anchor
from .BaseMaterial import BaseMaterial
from .Loads import Loads
from .Options import Options
from .Profile import Profile
from .ShearLug import ShearLug
from .Stiffeners import Stiffeners
from .Welds import Welds

class DesignModel(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity',]
        submodules_list = [
        ]
        # Submodules
        self.AnchorPlate = AnchorPlate(basefile=basefile)
        self.AnchorLayout = AnchorLayout(basefile=basefile)
        self.Anchor = Anchor(basefile=basefile)
        self.BaseMaterial = BaseMaterial(basefile=basefile)
        self.Loads = Loads(basefile=basefile)
        self.Options = Options(basefile=basefile)
        self.Profile = Profile(basefile=basefile)
        self.ShearLug = ShearLug(basefile=basefile)
        self.Stiffeners = Stiffeners(basefile=basefile)
        self.Welds = Welds(basefile=basefile)
        super().__init__(basefile, headerpath, submodules_list)