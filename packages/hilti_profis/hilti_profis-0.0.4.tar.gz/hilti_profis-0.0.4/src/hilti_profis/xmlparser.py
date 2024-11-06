import xmltodict

from pathlib import Path
from hilti_profis.utils.logger import log

def _dict_to_xml(dictionary: dict) -> str:
    """generate XML from dict"""
    return xmltodict.unparse(dictionary, pretty=True)

def save_xml(filepath: Path|str, data: dict|str) -> None:
    """Write XML to file"""
    if isinstance(data, dict):
        data = _dict_to_xml(data)
    log.info(f'Writing XML file to {filepath}')
    __write(data=data, filepath=filepath)

def read_xml(filepath: Path|str) -> dict:
    """Read XML file"""
    log.info(f'Reading XML file from {filepath}')
    with open(filepath, 'r') as f:
        return _xml_to_dict(f.read())

def _xml_to_dict(xml_string: str) -> dict:
    xml_dict = xmltodict.parse(xml_string, process_namespaces=False)
    return xml_dict

def __write(filepath: Path|str, data) -> None:
    """Write to file"""
    with open(filepath, 'w') as f:
        f.write(data)

def xml_content(data: dict|str) -> str|None:
    """Write XML to file"""
    if isinstance(data, dict):
        return _dict_to_xml(data)
