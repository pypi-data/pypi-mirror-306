import datetime
from typing import Callable, Dict, Any, Union

from .utils import Chrono


class Test:
    def __init__(self, func : Callable[[], Dict[str, Any]], parent : Union['TestList', 'Suite'] = None):
        self.__func = func
        self.__name = func.__annotations__["name"]
        self.__failed = False
        self.__error = False
        self.__skipped = False
        self.__time = 0.0
        self.__message = ""
        self.__traceback = None
        self.__output = None
        self.__parent = parent
        
    def run(self) -> bool:
        if self.__skipped:
            return False# Do not run the test if it was marked as skipped
        chrono = Chrono()
        with chrono:
            data = self.__func() # contains keys: error, failed, exception, traceback, output
        self.__time = chrono.get()
        self.__failed = data['failed']
        self.__error = data['error']
        self.__exceptionType = data["exception"].__class__.__name__ if data["exception"] is not None else ""
        self.__message = data["exception"].__str__() if data["exception"] is not None else ""
        self.__traceback = data["traceback"]
        self.__output = data["output"]
        
        if self.__parent is not None:
            self.__parent.update()
        
        return self.__failed or self.__error
            
    def completeName(self):
        if self.__parent is None:
            return self.__name
        return self.__parent.completeName() + "." + self.__name

        
    def skip(self, message : str):
        self.__skipped = True
        self.__message = message
        
    @property
    def name(self):
        return self.__name
    
    @property
    def failed(self):
        return self.__failed
    
    @property
    def error(self):
        return self.__error
    
    @property
    def skipped(self):
        return self.__skipped
    
    @property
    def time(self):
        return self.__time  
    
    @property
    def message(self):
        return self.__message
    
    @property
    def traceback(self):
        return self.__traceback
    
    @property
    def output(self):
        return self.__output
    
    @property
    def exceptionType(self):
        return self.__exceptionType
    
    @property
    def doc(self):
        return self.__func.__doc__
    
    def __str__(self):
        return f"{self.name} - {self.time} seconds - {'Failed' if self.failed else 'Succeeded'} - {'Error' if self.error else 'No error'} - {'Skipped' if self.skipped else 'Not skipped'}"
    
    

TESTLIST = None

class TestList:
    def __init__(self, name : str, parent : Union['TestList', 'Suite'] = None):
        self._timestamp = datetime.datetime.now() # Date and time of when the test run was executed
        self._name = name
        self._tests = 0
        self._failures = 0
        self._errors = 0
        self._skipped = 0
        self._time = 0.0
        self._childs = {} #type: Dict[str, Union[Test, Suite]]
        self._parent = parent
        
    def hasChild(self, name : str):
        return name in self._childs
    
    def getChild(self, name : str):
        return self._childs[name]
        
    def addTest(self, test : Test):
        self._childs[test.name] = test
        self._tests += 1
        self._failures += 1 if test.failed else 0
        self._errors += 1 if test.error else 0
        self._skipped += 1 if test.skipped else 0
        self._time += test.time
        
    def addSuite(self, suite: 'Suite'):
        self._childs[suite.name] = suite
        self._tests += suite.tests
        self._failures += suite.failures
        self._errors += suite.errors
        self._skipped += suite.skipped
        self._time += suite.time
        
    def run(self) -> bool:
        failed = False
        for child in self._childs.values():
            failed = failed or child.run()
        return failed
    
    def update(self):
        self._tests = 0
        self._failures = 0
        self._errors = 0
        self._skipped = 0
        self._time = 0.0
        for child in self._childs.values():
            if isinstance(child, Test):
                self._tests += 1
                self._failures += 1 if child.failed else 0
                self._errors += 1 if child.error else 0
                self._skipped += 1 if child.skipped else 0
                self._time += child.time
            else:
                self._tests += child.tests
                self._failures += child.failures
                self._errors += child.errors
                self._skipped += child.skipped
                self._time += child.time
        
        if self._parent is not None:
            self._parent.update()
            
    def completeName(self):
        if self._parent is None:
            return self._name
        return self._parent.completeName() + "." + self._name
        
    @property
    def timestamp(self):
        return self._timestamp
    
    @property
    def name(self):
        return self._name
    
    @property
    def tests(self):
        return self._tests
    
    @property
    def failures(self):
        return self._failures
    
    @property
    def errors(self):
        return self._errors
    
    @property
    def skipped(self):
        return self._skipped
    
    @property
    def time(self):
        return self._time
    
    @property
    def childs(self):
        return self._childs        

    @staticmethod
    def getInstance():
        global TESTLIST
        if TESTLIST is None:
            raise Exception("TestList instance not created")
        return TESTLIST
    
    @staticmethod
    def new(name : str):
        global TESTLIST
        TESTLIST = TestList(name)
        return TESTLIST
    
    def __str__(self):
        return "TestList : " + self.name + "\n" + "\n".join([str(child) for child in self.childs.values()])
    
    def getHierarchy(self) -> Dict[str, Union[Dict, str]]: # Returns a dictionary with the hierarchy of it's children
        result = {}
        for child in self.childs.values():
            if isinstance(child, Test):
                result[child.name] = child.name
            else:
                result[child.name] = child.getHierarchy()
        return result


class Suite(TestList):
    def __init__(self, file : str, name : str = None, parent : Union['TestList', 'Suite'] = None):
        super().__init__(name if name is not None else file, parent)
        self._file = file
        
    @property
    def file(self):
        return self._file
    
    def __str__(self):
        return f"Suite {self.name} ({self.file}) : {self.tests} tests, {self.failures} failures, {self.errors} errors, {self.skipped} skipped, {self.time} seconds"


class ReturnCodeError(Exception):
    pass