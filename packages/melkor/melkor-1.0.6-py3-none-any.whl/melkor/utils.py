import builtins
import traceback
import time


class CapturePrint:
    def __init__(self):
        self.__stdout = [] #type: list[str]
        
    def __enter__(self):
        self.__buildinPrint = builtins.print
        builtins.print = self.__print
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        builtins.print = self.__buildinPrint
        
    def __print(self, *args, **kwargs):
        self.__stdout.append(" ".join(str(args)))
        
    def get(self) -> list[str]:
        return self.__stdout
    
    
def formatTraceback(exception: Exception) -> str:
    """Format the traceback of an exception, removing the first element"""
    trace =  traceback.TracebackException.from_exception(exception)
    trace.stack.pop(0)
    return "    ".join(trace.format())


class Chrono:
    def __init__(self):
        self.__start = None
        self.__end = None
    
    def __enter__(self):
        self.__start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__end = time.time()
        
    def get(self):
        if self.__end is None: # Get the value of the chrono, without stopping it
            return time.time() - self.__start
        return self.__end - self.__start
