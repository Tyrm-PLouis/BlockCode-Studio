from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *
import keyword
import pkgutil
from pathlib import Path
import os



class Menu:
    def __init__(self, window: QMainWindow):
        self.window = window
        
        self.FILE_MENU : QMenu = QMenu("File")
        self.EDIT_MENU : QMenu = QMenu("Edit")
        self.addActionToMenu(self.FILE_MENU, "New", "Ctrl+N", self.new_file)
        self.addActionToMenu(self.FILE_MENU, "Open File", "Ctrl+O", self.open_file)
        self.addActionToMenu(self.FILE_MENU, "Open Folder", "Ctrl+K", self.open_folder)
        self.FILE_MENU.addSeparator()
        self.addActionToMenu(self.FILE_MENU, "New Project", "Ctrl+Shift+N", self.new_project)
        self.addActionToMenu(self.FILE_MENU, "Open Project", "Ctrl+Shift+O", self.open_project)
        self.FILE_MENU.addSeparator()
        self.addActionToMenu(self.FILE_MENU, "Save", "Ctrl+S", self.save_file)
        self.addActionToMenu(self.FILE_MENU, "Save As", "Ctrl+Shift+S", self.save_as)
        
        self.addActionToMenu(self.EDIT_MENU, "Copy", "Ctrl+C", self.copy)


    def addActionToMenu(self, menu : QMenu, action_name : str, action_shortcut : str, action_callback):
        action = menu.addAction(action_name)
        action.setShortcut(action_shortcut)
        action.triggered.connect(action_callback)
        
    def new_file(self):
        self.window.set_new_tab(Path("Untitled"), is_new_file=True)
                        
    def save_file(self):
        if self.window.current_file is None and self.window.tab_view.count() > 0:
            self.save_as()
        
        editor = self.window.tab_view.currentWidget()
        self.window.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.window.current_file.name}", 2000)
        editor.current_file_changed = False
        
    def save_as(self):
        editor = self.window.tab_view.currentWidget()
        if editor is None:
            return
        
        file_path = QFileDialog.getSaveFileName(self.window, "Save As", os.getcwd())[0]
        if file_path is None:
            self.window.statusBar().showMessage("Canceled", 2000)
            return
        path = Path(file_path)
        path.write_text(editor.text())
        self.window.tab_view.setTabText(self.window.tab_view.currentIndex(), path.name)
        self.window.statusBar().showMessage(f"Saved {path.name}",2000)
        self.window.current_file = path
        editor.current_file_changed = False
        
    def open_file(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        
        new_file = QFileDialog.getOpenFileName(self.window,
                                               "Pick a File", "", "All Files (*);; Python Files (*.py)",
                                               options=ops)
        print(new_file)
        if new_file[0] == '':
            self.window.statusBar().showMessage("Canceled", 2000)
            return
        f = Path(new_file[0])
        self.window.set_new_tab(f)
        
    def open_folder(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        
        new_folder = QFileDialog.getExistingDirectory(self, "Pick a Folder", "", options=ops)
        if new_folder:
            self.window.model.setRootPath(new_folder)
            self.window.tree_view.setRootIndex(self.window.model.index(new_folder))
            self.window.statusBar().showMessage(f"Opened {new_folder}", 2000)
    
    def copy(self):
        editor = self.window.tab_view.currentWidget()
        if editor is not None:
            editor.copy()
            
    def new_project(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        
        new_project = QFileDialog.getOpenFileNames
        ...
        
    def open_project(self):
        ...




