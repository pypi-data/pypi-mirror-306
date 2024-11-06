import pytest

from hilti_profis.main import PE

@pytest.fixture(scope='module')
def anchor():
    return PE()

def test_Model(anchor):
    assert len(list(anchor.Model.data.keys())) >= 1
    
def test_Anchor(anchor):
    assert len(list(anchor.Model.Anchor.data.keys())) >= 1
    assert anchor.Model.Anchor.data != anchor.Model.data
    
def test_AnchorPlate(anchor):
    assert len(list(anchor.Model.AnchorPlate.data.keys())) >= 1
    assert len(list(anchor.Model.AnchorPlate.Ledger.data.keys())) >= 1
    assert len(list(anchor.Model.AnchorPlate.Custom.data.keys())) >= 1
    assert anchor.Model.AnchorPlate.data != anchor.Model.data
    
def test_AnchorLayout(anchor):
    assert len(list(anchor.Model.AnchorLayout.data.keys())) >= 1
    assert len(list(anchor.Model.AnchorLayout.Points.data.keys())) >= 1
    assert anchor.Model.AnchorLayout.data != anchor.Model.data
    
def test_BaseMaterial(anchor):
    assert len(list(anchor.Model.BaseMaterial.data.keys())) >= 1
    assert len(list(anchor.Model.BaseMaterial.SupplementaryRebar.data.keys())) >= 1
    assert anchor.Model.BaseMaterial.data != anchor.Model.data

def test_Loads(anchor):
    assert len(list(anchor.Model.Loads.data.keys())) >= 1
    assert len(list(anchor.Model.Loads.Combos.data.keys())) >= 1
    assert isinstance(anchor.Model.Loads.Combos['LoadCombinationEntity'], dict)
    assert anchor.Model.Loads.data != anchor.Model.data
    
def test_Options(anchor):
    assert len(list(anchor.Model.Options.data.keys())) >= 1
    assert anchor.Model.Options.data != anchor.Model.data
    
def test_Profile(anchor):
    assert len(list(anchor.Model.Profile.data.keys())) >= 1
    assert len(list(anchor.Model.Profile.Custom.data.keys())) >= 1
    assert anchor.Model.Profile.data != anchor.Model.data

def test_ShearLug(anchor):
    assert len(list(anchor.Model.ShearLug.data.keys())) >= 1
    assert anchor.Model.ShearLug.data != anchor.Model.data
    
def test_Stiffeners(anchor):
    assert len(list(anchor.Model.Stiffeners.data.keys())) >= 1
    assert len(list(anchor.Model.Stiffeners.Custom.data.keys())) >= 1
    assert anchor.Model.Stiffeners.data != anchor.Model.data
    
def test_Welds(anchor):
    assert len(list(anchor.Model.Welds.data.keys())) >= 1
    assert anchor.Model.Welds.data != anchor.Model.data
    