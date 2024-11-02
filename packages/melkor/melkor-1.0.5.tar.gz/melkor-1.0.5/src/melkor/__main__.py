import argparse
import sys
import os
import importlib.metadata as metadata
import traceback


from gamuLogger import Logger, LEVELS

from .settings import Settings
from .engine import importFiles
from .customTypes import TestList
from .output.junit import Report as JunitReport

Logger.setModule("melkor")
    

def addSourcePath(sourceDir : str):
    sourceDir = os.path.abspath(sourceDir)
    sys.path.append(sourceDir)
    Logger.debug(f"Added '{sourceDir}' to the source path")


    
    
def run(configFilePath : str):
    
    Logger.debug(f"melkor version: {metadata.version('melkor')}")
    
    Settings.setFilePath(configFilePath)
        
    testDir = Settings().get("testDir")
    if not os.path.exists(testDir):
        Logger.error(f"Test directory '{testDir}' not found")
        sys.exit(1)
        
    sourceDir = Settings().get("sourceDir")
    if not os.path.exists(sourceDir):
        Logger.error(f"Source directory '{sourceDir}' not found")
        sys.exit(1)
        
    addSourcePath(sourceDir)

    TestList.new(Settings().get("name"))

    files = [os.path.join(testDir, file) for file in os.listdir(testDir) if file.endswith(".py")]
    Logger.info(f"Found {len(files)} test files, loading them")
    importFiles(files)
    
    Logger.info("Running tests")
    hasfailed = TestList.getInstance().run()
    
    Logger.info("Generating JUnit report")
    junitReport = JunitReport(TestList.getInstance())
    junitReport.save(Settings().get("outFile"))
    Logger.info(f"Report generated to {Settings().get('outFile')}")
    
    if hasfailed:
        return 1
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="Path to the configuration file")
    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    
    if args.debug:
        Logger.setLevel('stdout', LEVELS.DEBUG)
        
    
    Logger.debug(f"Python version: {sys.version}")
    Logger.debug(f"gamuLogger version: {metadata.version('gamuLogger')}")
    
    return run(args.configFile)


if __name__ == "__main__":
    try:
        exit(main())
    except Exception as e:
        Logger.debug(traceback.format_exc())
        Logger.critical(f"An exception occurred: {e}")
        exit(1)
