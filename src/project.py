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

        adv = "advancement"

        tags_folders = [mc_function]

        tags = ("tags", tags_folders)

        mc_folders = [tags]
        dp_folders = [function, adv, "recipe"]

        mc_ns = ("minecraft", mc_folders)
        dp_namespace = (self.namespace, dp_folders)

        self.namespaces = [mc_ns, dp_namespace]
        dp_root = ("data", self.namespaces)

    def get_namespaces(self):
        return self.namespaces

    def test(self) -> str:
        print("écriture de text.txt")
        return "test.txt"

    def ns_main(self, root) -> str:
        print(root + " from ns_main")
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
                        
    def CreateDir(self, root, l):
        for t in l:
            if type(t) is tuple:
                if type(t[1]) in [list, tuple]:
                    r = root + "/" + t[0]
                    self.CreateDir(r, t[1])
                    continue
                root += "/" + t[0]
                if not os.path.exists(f"{root}/{t[1]}"):
                    os.makedirs(f"{root}/{t[1]}")
            else:
                if callable(t):
                    t(root)
                    if not os.path.exists(f"{root}/{t(root)}"):
                        os.makedirs(f"{root}/{t(root)}")
                    continue
                if not os.path.exists(f"{root}/{t}"):
                    os.makedirs(f"{root}/{t}")



        
#ProjectGenerator.printDir(ProjectGenerator.root, ProjectGenerator.get_namespaces())






# class TreePath(object):
#     def __init__(self, name = "root", children = None) -> None:
#         self.name = name
#         self.children = []
#         if children is not None:
#             for child in children:
#                 self.add_child(child)
                
#     def __repr__(self) -> str:
#         return "/" + self.name

#     def add_child(self, node):
#         assert isinstance(node, TreePath)
#         self.children.append(node)