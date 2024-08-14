from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *

from pathlib import Path
import shutil
import os
import sys
import subprocess

from ui.editor import Editor


class FileManager(QTreeView):
    def __init__(self, tab_view, set_new_tab = None, main_window = None):
        super(FileManager, self).__init__(None)
        
        self.set_new_tab = set_new_tab
        self.tab_view = tab_view
        self.main_window = main_window
        
        # Variables pour les fonctionnalités de renommage
        # ...
        
        self.manager_font = QFont('Arial', 13)

        # create file system model to show in tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        
        # File system filters
        self.model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.Drives)
        self.model.setReadOnly(False)
        
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        self.setFont(self.manager_font)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(os.getcwd()))
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        # Add custom context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        # Handling click
        self.clicked.connect(self.tree_view_clicked)
        self.setIndentation(10)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Hide header and hide other columns except for name
        self.setHeaderHidden(True)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        
        # Drag & Drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        
        # Editer les noms de fichiers
        
        self.previous_rename_name = None
        self.is_renaming = False
        self.current_edit_index = None
        
        self.itemDelegate().closeEditor.connect(self._on_closeEditor)
        
    def show_context_menu(self, pos: QPoint):
        index = self.indexAt(pos)
        menu = QMenu()
        menu.addAction("New File")
        menu.addAction("New Folder")
        menu.addAction("Open In File Manager")
        
        if index.column() == 0:
            menu.addAction("Rename")
            menu.addAction("Delete")
            
        action = menu.exec_(self.viewport().mapToGlobal(pos))
        
        if not action:
            return
        
        if action.text() == "Rename":
            self.action_rename(index)
        elif action.text() == "Delete":
            self.action_delete(index)
        elif action.text() == "New Folder":
            self.action_new_folder()
        elif action.text() == "New File":
            self.action_new_file(index)
        elif action.text() == "Open In File Manager":
            self.action_open_in_file_manager(index)
        else:
            pass
    
    def _on_closeEditor(self, editor: QLineEdit):
        if self.is_renaming:
            self.rename_file_with_index()
            
    def action_new_folder(self):
        f = Path(self.model.rootPath()) / "New Folder"
        count = 1
        while f.exists():
            f = Path(f.parent / f"New Folder_{count}")
            count += 1
        index = self.model.mkdir(self.rootIndex(), f.name)
        self.edit(index)
        
    
    def action_rename(self, index):
        self.edit(index)
        self.previous_rename_name = self.model.fileName(index)
        self.is_renaming = True
        self.current_edit_index = index
        
    def delete_file(self, path: Path):
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        
    def action_delete(self, index):
        file_name = self.model.fileName(index)
        dialog = self.show_dialog(
            "Delete", f"Are you sure you want to delete {file_name}"
        )
        if dialog == QMessageBox.StandardButton.Yes:
            if self.selectionModel().selectedRows():
                path = Path(self.model.filePath(index))
                self.delete_file(path)
                for editor in self.tab_view.findChildren(Editor):
                    if editor.path.name == path.name:
                        self.tab_view.removeTab(
                            self.tab_view.indexOf(editor)
                        )
                        
    def action_new_file(self, index: QModelIndex):
        root_path = self.model.rootPath()
        if index.column() != -1 and self.model.isDir(index):
            self.expand(index)
            root_path = self.model.filePath(index)
        
        f = Path(root_path) / "file"
        count = 1
        while f.exists():
            f = Path(f.parent / f"file_{count}")
            count += 1
        f.touch()
        index = self.model.index(str(f.absolute()))
        self.edit(index)
        
    def action_open_in_file_manager(self, index: QModelIndex):
        path = os.path.abspath(self.model.filePath(index))
        is_dir = self.model.isDir(index)
        if os.name == "nt":
            if is_dir:
                subprocess.Popen(f'explorer "{path}"')
            else:
                subprocess.Popen(f'explorer /select,"{path}"')
        elif os.name == "posix":
            if sys.platform == "darwin":
                if is_dir:
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["open", "-R", path])
            else:
                subprocess.Popen(["xdg-open", os.path.dirname(path)])
        else:
            raise OSError(f"Unsupported platform {os.name}")
        
    def show_dialog(self, title, msg) -> int:
        dialog = QMessageBox(self)
        dialog.setFont(self.manager_font)
        dialog.font().setPointSize(14)
        dialog.setWindowTitle(title)
        dialog.setWindowIcon(QIcon(":/assets/icons/close-icon.svg"))
        dialog.setText(msg)
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QMessageBox.StandardButton.No)
        dialog.setIcon(QMessageBox.Icon.Warning)
        return dialog.exec_()
        
    def rename_file_with_index(self):
        new_name = self.model.fileName(self.current_edit_index)
        if self.previous_rename_name == new_name:
            return
        for editor in self.tab_view.findChildren(Editor):
            if editor.path.name == self.previous_rename_name:
                editor.path = editor.path.parent / new_name
                self.tab_view.setTabText(
                    self.tab_view.indexOf(editor), new_name
                )
                self.tab_view.repaint()
                editor.full_path = editor.path.absolute()
                self.main_window.current_file = editor.path
                break
        
    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        
        if p.is_file():
            self.set_new_tab(p)
        
        
    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()
            
    def dropEvent(self, e: QDropEvent) -> None:
        root_path = Path(self.model.rootPath())
        if e.mimeData().hasUrls():
            for url in e.mimeData().urls():
                path = Path(url.toLocalFile())
                if path.is_dir():
                    shutil.copytree(path, root_path / path.name)
                else:
                    if root_path.samefile(self.model.rootPath()):
                        index: QModelIndex = self.indexAt(e.pos())
                        if index.column() == -1:
                            shutil.move(path, root_path / path.name)
                        else:
                            folder_path = Path(self.model.filePath(index))
                            shutil.move(path, folder_path / path.name)
                    else:
                        shutil.copy(path, root_path / path.name)
        e.accept()
        
        return super().dropEvent(e)