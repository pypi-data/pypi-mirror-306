import json5 as json
import os

class Settings:
    """
    Read-only settings class that reads a JSON file and provides access
    """
    __instance = None
    __configFile = 'melkor.json'
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance
    
    def __init__(self):
        self.__data = {}
        self.load()
        
    def load(self):
        if not os.path.exists(Settings.__configFile):
            raise FileNotFoundError(f"Settings file '{Settings.__configFile}' not found")
        with open(Settings.__configFile, 'r') as file:
            self.__data = json.load(file)
            
    def get(self, key : str, default = None):
        tokens = key.split('.')
        data = self.__data
        try:
            for token in tokens:
                data = data[token]
            return data
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Key '{key}' not found in settings")
            
    
    def __getitem__(self, key : str):
        return self.get(key)
    
    def __contains__(self, key : str):
        try:
            self.get(key)
            return True
        except KeyError:
            return False
        
    def has(self, key : str):
        return key in self
    
    @staticmethod
    def setFilePath(path : str):
        Settings.__configFile = path
        
        
            
        
    