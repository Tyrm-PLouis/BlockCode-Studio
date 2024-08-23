import pathlib
from scripts.project import ProjectGenerator
# DP = Data Pack, RP = Resource Pack

class ResourcePack():
    # rp 1.21 : 34
    def __init__(self, name : str = "new resource pack", namespace : str = "", version : int = 34, description : str = "", path : str = "") -> None:
        self.name = name
        self.namespace = namespace if namespace else name
        self.version = version
        self.description = description
        self.resource_pack_path = path
        self.mc_generator = ProjectGenerator(self.namespace)
        
    def setMcMeta(self):
        with open(f'{self.resource_pack_path}/pack.mcmeta', 'w+') as mcmeta_file:
            text = {
                "pack": {
                    "pack_format": self.version,
                    "description": self.description
                }
            }
            mcmeta_file.write(text)
    
    def createRoot(self):
        """
        Create minecraft namespace and custom one
        """
        self.mc_generator.CreateDir(f"{self.resource_pack_path}/{self.name}", self.mc_generator.rp_root)
        self.setMcMeta()
        