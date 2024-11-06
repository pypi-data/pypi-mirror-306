
from pathlib import Path

from hilti_profis import xmlparser
from hilti_profis.Model import DesignModel
from hilti_profis.utils.logger import log

class PE:
    def __init__(self, basefile: Path|str|None = None, disable_logging: bool=False) -> None:
        self.basefile: Path|str = basefile or Path(__file__).parent / 'basefile.pe'
        self.Model = DesignModel(basefile=xmlparser.read_xml(self.basefile))
        if disable_logging:
            log.setLevel(40)
        
    def __repr__(self) -> str:
        return f'PE(basefile={self.basefile})'
    
    def __str__(self) -> str:
        return "Hilti Profis file generation module"
        
    def __apply_baseconfig(self) -> dict:
        """Applies cofigs from basefile"""
        _new_dict = {'ProjectDesignConcreteEntity':self.Model.data}
        return self.__update_dict(
            base_dict=xmlparser.read_xml(filepath=self.basefile),
            override_dict=_new_dict)

    def save(self, filepath: Path|str):
        """Saves the modified config to file"""
        return xmlparser.save_xml(filepath=filepath, data=self.__apply_baseconfig())

    def __update_dict(self, base_dict: dict, override_dict: dict) -> dict:
        """Applies dict values from `override_dict` to `base_dict`"""
        override_dict = override_dict.copy()
        for kb, vb in base_dict.items():
            ko = kb
            vo = override_dict.get(ko)
            if vo is None:
                vo = vb
            if isinstance(vb, dict) and isinstance(vo, dict):
                kb = self.__update_dict(vb, vo)
            else:
                override_dict[ko] = vo
        return override_dict
    
    def xml_content(self) -> str|None:
        """Returns Str contents of XML file"""
        return xmlparser.xml_content(data=self.__apply_baseconfig())