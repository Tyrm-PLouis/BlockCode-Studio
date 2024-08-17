from dataclasses import dataclass
from pathlib import Path
import json

root = "root"
namespace = "mySpace"

tick_data = {
    "values": [
        f"{namespace}:main"
    ]
}

load_data = {
    "values": [
        f"{namespace}:load"
    ]
}

def test() -> str:
    print("écriture de text.txt")
    return "test.txt"

def ns_main(root) -> str:
    print(root + " from ns_main")
    # with open(root + "/main.mcfunction", "w+") as f:
    #      f.write("")
    return "main.mcfunction"

def ns_load(root) -> str:
    # with open(root + "/load.mcfunction", "w+") as f:
    #      f.write("")
    return "load.mcfunction"

def mc_tick(root) -> str:
    # with open(root + "/tick.json", "w+") as f:
    #     json.dump(tick_data, f, ensure_ascii=False, indent=4)
    return "tick.json"

def mc_load(root) -> str:
    # with open(root + "/load.json", "w+") as f:
    #     json.dump(load_data, f, ensure_ascii=False, indent=4)
    return "load.json"

mc_function = ("function", [mc_tick, mc_load])

function = ("function", [ns_main, ns_load])

adv = "advancement"

tags_folders = [mc_function]

tags = ("tags", tags_folders)

mc_folders = [tags]
dp_folders = [function, adv, "recipe"]

dp_namespace = (namespace, dp_folders)
mc_ns = ("minecraft", mc_folders)

namespaces = [mc_ns, dp_namespace]

dp_root = ("data", namespaces)

"""
(str, list<str>) = folder with subfolders/files
"""


def printDir(root, l):
    for t in l:
        if type(t) is tuple:
            if type(t[1]) in [list, tuple]:
                r = root + "/" + t[0]
                printDir(r , t[1])
                continue
            
            root += "/" + t[0]
            print(f"{root}/{t[1]}")
        else:
            if callable(t):
                print(f"{root}/{t(root)}")
                continue
            print(f"{root}/{t}")
            
printDir(root, namespaces)













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