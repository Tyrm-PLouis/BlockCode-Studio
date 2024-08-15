from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem

import os
from pathlib import Path
import re

#############################
##### SEARCH ITEM CLASS #####
#############################
class SearchItem(QListWidgetItem):
    """
    This class represents a searched item trough the search bar
    
    Attributes :
        name [str]: name of the file where the text has been located
        full_path [str]: absolute path to the file
        line_n [int]: line index where text is located in file
        end [int]: string index where text ends
        line [str]: line in which is located the text
    """
    def __init__(self, name, full_path, line_n, end, line):
        self.name = name
        self.full_path = full_path
        self.line_n = line_n
        self.end = end
        self.line = line
        self.formatted = f'{self.name}:{self.line_n}:{self.end} - {self.line} ...'
        super().__init__(self.formatted)
        
    def __str__(self) -> str:
        return self.formatted
    
    def __repr__(self) -> str:
        return self.formatted
    
#############################
#### SEARCH WORKER CLASS ####
#############################
class SearchWorker(QThread):
    """
    This class will run the search feature in a separate thread
    """
    finished = pyqtSignal(list)
    
    def __init__(self):
        super(SearchWorker, self).__init__(None)
        self.items = []
        self.search_path: str = None
        self.search_text: str = None
        self.search_project: bool = None
        
    def is_binary(self, path):
        """
        Check if file is binary
        """
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
        
    def walkdir(self, path, exclude_dirs: list, exclude_files: list):
        for root, dirs, files in os.walk(path, topdown=True):
            # filtrage
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            files[:] = [f for f in files if Path(f).suffix not in exclude_files]
            yield root, dirs, files
        
    def search(self):
        debug = False
        self.items = []
        # Directories to ignore in the search
        exclude_dirs = set([".git", ".svn", ".hg", ".bzr", ".idea", "__pycache__", "venv"])
        if self.search_project:
            exclude_dirs.remove("venv")
        # File extensions to ignore
        exclude_files = set([".svg", ".png", ".exe", ".pyc", ".qm"])
        
        for root, _, files in self.walkdir(self.search_path, exclude_dirs, exclude_files):
            # limite totale de recherche
            if len(self.items) > 5_000:
                break
            for file in files: 
                full_path = os.path.join(root, file)
                if self.is_binary(full_path):
                    break
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        try:
                            reg = re.compile(self.search_text, re.IGNORECASE)
                            for i, line in enumerate(f):
                                if m := reg.search(line):
                                    fd = SearchItem(
                                        file,
                                        full_path,
                                        i,
                                        m.end(),
                                        line[m.start():].strip()[:50]
                                    )
                                    self.items.append(fd)
                        except re.error as e:
                            if debug: print(e)
                except UnicodeDecodeError as e:
                    if debug: print(e)
                    continue
        self.finished.emit(self.items)
        
    def run(self):
        self.search()
        
    def update(self, pattern, path, search_project):
        self.search_text = pattern
        self.search_path = path
        self.search_project = search_project
        self.start()