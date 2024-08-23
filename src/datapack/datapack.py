import pathlib
import os
import json


from scripts.project import ProjectGenerator

# DP = Data Pack, RP = Resource Pack

class Datapack():
    def __init__(self, name : str = "new datapack", namespace : str = "", version : int = 48, description : str = "", path : str = "", rp_path : str = None) -> None:
        self.name = name
        self.namespace = namespace.lower() if namespace else self.name.lower()
        self.version = version
        self.description = description
        self.datapack_path = path
        self.resource_pack_path = rp_path
        self.mc_generator = ProjectGenerator(self.namespace)
        
        #self.setMcMeta()
        
    def setResourcePack(self, rp_path : str):
        self.resource_pack_path = rp_path
        
    def setMcMeta(self):
        with open(f'{self.datapack_path}/{self.name}/pack.mcmeta', 'w+') as mcmeta_file:
            text = f"""{{\n\t\"pack\": {{\n\t\t\"pack_format\": {self.version},\n\t\t\"description\": {self.description}\n\t}}\n}}"""
            mcmeta_file.write(text)
            
        
    def createRoot(self):
        """
        Create minecraft namespace and custom one
        """
        self.mc_generator.CreateDir(f"{self.datapack_path}/{self.name}", self.mc_generator.dp_root)
        self.setMcMeta()
        self.generate_settings()
        
    
    def generate_settings(self):
        
        settings_data = {
            "project_name": self.name,
            "namespace": self.namespace,
            "project_path": self.datapack_path + "/" + self.name,
            "rp_path": self.resource_pack_path
        }
        
        with open(f"{self.datapack_path}/{self.name}/settings.json", "w+") as f:
            json.dump(settings_data, f, ensure_ascii=False, indent=4)
    
    def addNamespace(self, variant_name : str):
        """
        Adds a namespace folder with a variant name as suffix : [namespace]_[variant], ex: mypack_blocks
        """
        p = f"{self.datapack_path}/{self.name}/data/{self.namespace}_{variant_name}"
        if not os.path.exists(p):
            os.mkdir(p)
        
        
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