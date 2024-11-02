import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from datetime import datetime

from gamuLogger import Logger

Logger.setModule("melkor")


from ..customTypes import Suite, Test, TestList


def formatDate(date: datetime) -> str:
    #return the date in the ISO 8601 format
    return date.strftime("%Y-%m-%dT%H:%M:%S")

class Report:
    def __init__(self, TestList: TestList):
        self.__testList = TestList
    
    def __generateTestElement(self, test: Test, className : str) -> ET.Element:
        Logger.debug(f"Generating test element for {test.name}")
        element = ET.Element("testcase")
        element.set("name", test.name)
        element.set("classname", className)
        element.set("time", str(test.time))
        if test.failed:
            failure = ET.Element("failure")
            failure.set("message", test.message)
            failure.set("type", test.exceptionType)
            failure.text = test.traceback
            element.append(failure)
        if test.error:
            error = ET.Element("error")
            error.set("message", test.message)
            error.set("type", test.exceptionType)
            error.text = test.traceback
            element.append(error)
        if test.skipped:
            skipped = ET.Element("skipped")
            skipped.set("message", test.message)
            element.append(skipped)
        
        output = test.output
        if output:

            systemOut = ET.Element("system-out")
            systemOut.text = '\n'.join(output)
            element.append(systemOut)
            
        if test.doc:
            doc = ET.Element("property")
            doc.set("name", "description")
            doc.set("value", test.doc)
            element.append(doc)
        
        Logger.debug(f"Generated test element for {test.name}")
        return element
    
    def __generateSuiteElement(self, suite: Suite) -> ET.Element:
        Logger.debug(f"Generating suite element for {suite.name}")
        element = ET.Element("testsuite")
        element.set("name", str(suite.name))
        element.set("tests", str(suite.tests))
        element.set("failures", str(suite.failures))
        element.set("errors", str(suite.errors))
        element.set("skipped", str(suite.skipped))
        element.set("time", str(suite.time))
        element.set("timestamp", formatDate(suite.timestamp))
        element.set("file", suite.file)
        for child in suite.childs.values():
            if isinstance(child, Suite):
                element.append(self.__generateSuiteElement(child))
            else:
                element.append(self.__generateTestElement(child, suite.name))
        return element
    
    def __generateSuitesElement(self, testList: TestList) -> ET.Element:
        Logger.debug(f"Generating suites element for {testList.name}")
        element = ET.Element("testsuites")
        element.set("name", str(testList.name))
        element.set("tests", str(testList.tests))
        element.set("failures", str(testList.failures))
        element.set("errors", str(testList.errors))
        element.set("skipped", str(testList.skipped))
        element.set("time", str(testList.time))
        element.set("timestamp", formatDate(testList.timestamp))
        for child in testList.childs.values():
            if isinstance(child, Suite):
                element.append(self.__generateSuiteElement(child))
            else:
                element.append(self.__generateTestElement(child, testList.name))
        return element
    
    def generate(self) -> str:
        root = self.__generateSuitesElement(self.__testList)
        return minidom.parseString(ET.tostring(root)).toprettyxml()
    
    def save(self, path: str):
        with open(path, 'w') as file:
            file.write(self.generate())
            
