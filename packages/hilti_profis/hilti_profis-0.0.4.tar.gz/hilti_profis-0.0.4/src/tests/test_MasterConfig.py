from hilti_profis.Config import MasterModule
import pytest

@pytest.fixture(scope='module')
def cascading_module():
    basefile = {
        'a': 1,
        'b': {
            'x':11,
            'y':12,
            'z':{
                'p':21,
                'q':22,
                'r':23
            }
        },
        'c':3
    }
    class BaseMod(MasterModule):
        def __init__(self, basefile: dict) -> None:
            self.headerpath = []
            super().__init__(basefile, headerpath = self.headerpath, submodules_list=[SubMod(basefile=basefile)])

    class SubMod(MasterModule):
        def __init__(self, basefile: dict) -> None:
            self.headerpath = ['b']
            super().__init__(basefile, headerpath = self.headerpath, submodules_list=[SubSubMod(basefile=basefile)])

    class SubSubMod(MasterModule):
        def __init__(self, basefile: dict) -> None:
            self.headerpath = ['b', 'z']
            super().__init__(basefile, headerpath = self.headerpath)

    return BaseMod(basefile=basefile)
    
def test_data_inheritance1(cascading_module):
    cascading_module.SubMod['z']['r'] = 999
    cascading_module.SubMod.SubSubMod['r'] = 99
    cascading_module.SubMod['x'] = 98

    cascading_module.apply()
    assert cascading_module.modified_data == {'a': 1, 'b': {'x': 98, 'y': 12, 'z': {'p': 21, 'q': 22, 'r': 99}}, 'c': 3}

def test_data_inheritance2(cascading_module):
    cascading_module.SubMod.SubSubMod['r'] = 99
    cascading_module.SubMod['x'] = 98
    cascading_module.SubMod['z']['r'] = 999

    cascading_module.apply()
    assert cascading_module.modified_data == {'a': 1, 'b': {'x': 98, 'y': 12, 'z': {'p': 21, 'q': 22, 'r': 999}}, 'c': 3}

def test_data_inheritance3(cascading_module):
    cascading_module.SubMod.data['z']['r'] = 999
    cascading_module.SubMod.SubSubMod.data['r'] = 99
    cascading_module.SubMod.data['x'] = 98

    cascading_module.apply()
    assert cascading_module.modified_data == {'a': 1, 'b': {'x': 98, 'y': 12, 'z': {'p': 21, 'q': 22, 'r': 99}}, 'c': 3}

def test_data_inheritance4(cascading_module):
    cascading_module.SubMod.SubSubMod.data['r'] = 99
    cascading_module.SubMod.data['x'] = 98
    cascading_module.SubMod.data['z']['r'] = 999

    cascading_module.apply()
    assert cascading_module.modified_data == {'a': 1, 'b': {'x': 98, 'y': 12, 'z': {'p': 21, 'q': 22, 'r': 999}}, 'c': 3}