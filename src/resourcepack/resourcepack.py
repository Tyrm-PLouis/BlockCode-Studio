import pathlib
# DP = Data Pack, RP = Resource Pack

class ResourcePack():
    # rp 1.21 : 34
    def __init__(self, name : str = "new resource pack", version : int = 0, description : str = "", path : str = "") -> None:
        self.name = name
        self.version = version
        self.description = description
        self.resource_pack_path = path
        self.setMcMeta()
                
    def setMcMeta(self):
        with open(f'{self.resource_pack_path}/pack.mcmeta', 'w+') as mcmeta_file:
            text = {
                "pack": {
                    "pack_format": self.version,
                    "description": self.description
                }
            }
            mcmeta_file.write(text)