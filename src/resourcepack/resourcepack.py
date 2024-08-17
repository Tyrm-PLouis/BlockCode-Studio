import pathlib
# DP = Data Pack, RP = Resource Pack

class ResourcePack():
    def __init__(self, name : str = "new resource pack", version : int = 0, description : str = "", path : str = "") -> None:
        self.name = name
        self.version = version
        self.description = description
        self.resource_pack_path = path
        self.setMcMeta()
                
    def setMcMeta(self):
        mcmeta_file = open('pack.mcmeta', 'w')
        text = '{"pack": {"pack_format":' + self.version +',"description":"' + self.description + '"}}'
        mcmeta_file.write(text)
        mcmeta_file.close()