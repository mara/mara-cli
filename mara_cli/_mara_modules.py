"""Internal functions interacting with mara modules"""

import copy
from logging import Logger
import sys
from types import ModuleType
from typing import Callable, Dict, Iterable

import click


_mara_modules_imported = False

def import_mara_modules(log: Logger):
    """
    Import all installed mara modules

    Args:
        log: The application logger.
    """
    global _mara_modules_imported
    if _mara_modules_imported:
        return

    import pkg_resources
    import importlib

    for i in pkg_resources.working_set:
        package_name = i.key
        #version = i.version
        if package_name.startswith('mara-'):
            log.debug(f"Import module {package_name}")
            importlib.import_module(name=package_name.replace('-', '_'), package=package_name)
    
    _mara_modules_imported = True


def module_functionalities(module: ModuleType, MARA_XXX: str, type) -> []:
    """
    Returns some functionalities of a module that is declared in a MARA_XXX variable or function

    `module.MARA_XXX` can be
    - a function that returns a list or dict
    - a list
    - a dict
    """
    if MARA_XXX in dir(module):
        functionalities = getattr(module, MARA_XXX)
        if isinstance(functionalities, Callable):
            functionalities = functionalities()
        if isinstance(functionalities, Dict):
            functionalities = functionalities.values()
        if not isinstance(functionalities, Iterable):
            raise TypeError(
                f'{module.__name__}.{MARA_XXX} should be or return a list or dict of {type.__name__}. Got "{functionalities}".')
        for functionality in functionalities:
            if not isinstance(functionality, type):
                raise TypeError(f'In {module.__name__}.{MARA_XXX}: Expected a {type.__name__}, got "{functionality}"')
        return functionalities
    else:
        return []


def get_contributed_functionality(name: str, type) -> Dict[ModuleType, object]:
    """Gets the contributed functionality for one MARA_ variable"""
    for module in copy.copy(sys.modules).values():
        for obj in module_functionalities(module, name, click.Command):
            yield (module, obj)
