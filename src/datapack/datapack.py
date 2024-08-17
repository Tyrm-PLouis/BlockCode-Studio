import pathlib
import os
import json
# DP = Data Pack, RP = Resource Pack

class Datapack():
    def __init__(self, name : str = "new datapack", version : int = 0, description : str = "", path : str = "", rp_path : str = None) -> None:
        self.name = name
        self.version = version
        self.description = description
        self.datapack_path = path
        self.resource_pack_path = rp_path
        self.setMcMeta()
        
    def setResourcePack(self, rp_path : str):
        self.resource_pack_path = rp_path
        
    def setMcMeta(self):
        mcmeta_file = open('pack.mcmeta', 'w')
        text = {
            "pack": {
                "pack_format": self.version,
                "description": self.description
            }
        }
        mcmeta_file.write(text)
        mcmeta_file.close()
        
    def createRoot(self):
        """
        Create minecraft namespace and custom one
        """
        
    def addNamespace(self, variant_nam : str):
        """
        Adds a namespace folder with a variant name as suffix : [namespace]_[variant], ex: mypack_blocks
        """
        
    def addFunction(self):
        ...
        
    def addAdvancement(self):
        ...
        
    def addTags(self):
        ...
    
    def addRecipes(self):
        ...
        
    def addItemModifier(self):
        ...
        
    def addPredicate(self):
        ...
        
    def addStructure(self):
        ...
    
    def addLootTable(self):
        ...
        
    def addBlock(self):
        ...
        
    def addItem(self):
        ...
        
#https://minecraft.wiki/w/Data_pack