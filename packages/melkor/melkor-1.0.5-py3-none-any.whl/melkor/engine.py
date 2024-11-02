import importlib.util
from typing import List, Callable
import os

from gamuLogger import Logger

from .customTypes import TestList
from .settings import Settings


Logger.setModule("melkor")

def importFile(file) -> object:
    spec = importlib.util.spec_from_file_location("module.name", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def importFiles(files : List[str]) -> List[object]:
    result = []
    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File '{file}' not found")
        Logger.debug(f"Importing file '{file}'")
        result.append(importFile(file))
    return result


def runTests(testList : List[Callable[[], int]]) -> TestList:
    result = TestList(Settings.get("name"))
    
    for test in testList:
        data = test()
        if data["hasSucceeded"]:
            result['failedTests'] += 1
            string = f"Test {test.__annotations__['name']} failed"
            if data["exception"]:
                string += f" with exception: {data['exception']}"
            if data["output"]:
                string += "\nOutput:\n    " + '\n    '.join(data['output'])
            if data["traceback"]:
                string += "\nStack:\n    " + data['traceback']
            Logger.error(string)
            
            if not data["allowedToFail"]:
                result['failed'] = True
        
        else:
            Logger.debug(f"Test {test.__annotations__['name']} succeeded")
    
    return result
