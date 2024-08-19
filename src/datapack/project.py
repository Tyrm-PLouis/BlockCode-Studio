from dataclasses import dataclass
from pathlib import Path
import os
import json



"""
(str, list<str>) = folder with subfolders/files
"""

class ProjectGenerator():
    def __init__(self, namespace):
        self.namespace = namespace

        self.tick_data = {
            "values": [
                f"{self.namespace}:main"
            ]
        }

        self.load_data = {
            "values": [
                f"{self.namespace}:load"
            ]
        }
        mc_function = ("function", [self.mc_tick, self.mc_load])
        function = ("function", [self.ns_main, self.ns_load])

        tags_folders = [mc_function]

        tags = ("tags", tags_folders)

        mc_folders = [tags]
        dp_folders = [function]

        mc_ns = ("minecraft", mc_folders)
        dp_namespace = (self.namespace, dp_folders)

        self.namespaces = [mc_ns, dp_namespace]
        self.dp_root = ("data", self.namespaces)
        
        
        
        self.mc_atlases = ("atlases", {})
        self.mc_models = ("models", {})
        self.mc_textures = ("textures", {})
        self.rp_mc_folders = [self.mc_atlases, self.mc_models, self.mc_textures]
        
        self.rp_mc_ns = ("minecraft", self.rp_mc_folders)
        self.rp_ns = (self.namespace, self.rp_mc_folders)
        
        self.rp_namespaces = [self.rp_mc_ns, self.rp_ns]
        self.rp_root = ("assets", self.rp_namespaces)



    def get_namespaces(self):
        return self.namespaces

    def test(self) -> str:
        print("écriture de text.txt")
        return "test.txt"

    def ns_main(self, root) -> str:
        if not os.path.exists(root):
            os.makedirs(root)
        with open(root + "/main.mcfunction", "w+") as f:
             f.write("")
        return "main.mcfunction"

    def ns_load(self, root) -> str:
        if not os.path.exists(root):
            os.makedirs(root)
        with open(root + "/load.mcfunction", "w+") as f:
             f.write("")
        return "load.mcfunction"

    def mc_tick(self, root) -> str:
        if not os.path.exists(root):
            os.makedirs(root)
        with open(root + "/tick.json", "w+") as f:
            json.dump(self.tick_data, f, ensure_ascii=False, indent=4)
        return "tick.json"

    def mc_load(self, root) -> str:
        if not os.path.exists(root):
            os.makedirs(root)
        with open(root + "/load.json", "w+") as f:
            json.dump(self.load_data, f, ensure_ascii=False, indent=4)
        return "load.json"


    def printDir(self, root, l):
        for t in l:
            if type(t) is tuple:
                if type(t[1]) in [list, tuple]:
                    r = root + "/" + t[0]
                    self.printDir(r , t[1])
                    continue
                
                root += "/" + t[0]
                print(f"{root}/{t[1]}")
            else:
                if callable(t):
                    print(f"{root}/{t(root)}")
                    continue
                print(f"{root}/{t}")
                
    def alternatePrintDir(self, root, l):
        if type(l) in [tuple, list]:
            for t in l:
                if type(t) is str:
                    root += "/" + t
                    print(t + " is a string! " + root)
                elif callable(t):
                    print(f"{root} + {t(root)}")
                else:
                    self.alternatePrintDir(root, t)
                        
    def CreateDir(self, root, l):
        if type(l) in [tuple, list]:
            for t in l:
                if type(t) is str:
                    root += "/" + t
                    os.makedirs(root)
                    #print(t + " is a string! " + root)
                elif callable(t):
                    t(root)
                    if not os.path.exists(f"{root}/{t(root)}"):
                        os.makedirs(f"{root}/{t(root)}")
                else:
                    self.CreateDir(root, t)
        else:
            os.makedirs(f"{root}/{l}")

pr = ProjectGenerator("test")
pr.alternatePrintDir("root", pr.rp_root)