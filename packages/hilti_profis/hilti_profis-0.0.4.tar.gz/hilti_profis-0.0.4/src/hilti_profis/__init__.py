"Python binding for generating `.pe` files, for use with Hilti-Profis software."
__version__ = "0.0.4"

from .utils.logger import log
from hilti_profis.main import PE
from hilti_profis import xmlparser


log.info(f'{" Hilti Profis Module Started ":=^50}')

def debug(status=False):
    """Import this in a new module and enable debug to use debug
    example:
    ```python
    from template_python import debug
    debug(True)
    ```
    """
    if status:
        log.setLevel(10) #debug
    else:
        log.setLevel(20) #info

    log.debug(f'Debug Mode: {status}')
    
debug(status=False)