import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *

from pathlib import Path
import sys
import keyword
import pkgutil

from ui.editor import Editor

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.side_bar_clr = "#282c34"
        
        self.init_ui()
        
        self.current_file = None
        
    def init_ui(self):
        # Body
        self.setWindowTitle("TEXT EDITOR")
        self.resize(1300, 900)
        
        self.setStyleSheet(open("./src/css/style.qss", "r").read())
        
        self.window_font = QFont("Arial")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        
        
        self.set_up_menu()
        self.set_up_body()
        
        self.show()
        
    def set_up_menu(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)
        
        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)
        
        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)
        
        file_menu.addSeparator()
        
        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)
        
        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        
    def get_editor(self) -> QsciScintilla:
        editor = Editor()
        return editor
    
    def is_binary(self, path):
        '''
        Check if file is binary
        '''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
    
    def set_new_tab(self, path: Path, is_new_file=False):
        editor = self.get_editor()
        if is_new_file:
            self.tab_view.addTab(editor, "Untitled")
            self.setWindowTitle("Untitled")
            self.statusBar().showMessage("Openend Untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return
        
        if not path.is_file():
            return
        if not is_new_file and self.is_binary(path):
            self.statusBar().showMessage("Cannot open binary file!", 2000)
            return
        
        # Check if file is already open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return
                
        # Create new tab
        
        self.tab_view.addTab(editor, path.name)
        
        editor.setText(path.read_text())
        self.setWindowTitle(path.name)
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path.name}", 2000)

    def get_side_bar_label(self, path, name):
        label = QLabel()
        label.setPixmap(QPixmap(path).scaled(QSize(25, 25)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e, name)
        return label

    def set_up_body(self):
        
        # Body
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.Shape.NoFrame)
        body_frame.setFrameShadow(QFrame.Shadow.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0,0,0,0)
        body_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        body = QHBoxLayout()
        body.setContentsMargins(0,0,0,0)
        body.setSpacing(0)
        
        body_frame.setLayout(body)
        
        # Side bar
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Shadow.Plain)
        self.side_bar.setStyleSheet(f'''
                                    background-color: {self.side_bar_clr};
                                    ''')
        side_bar_layout = QHBoxLayout()
        side_bar_layout.setContentsMargins(5,10,5,0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        
        
        # Setup labels
        folder_label = self.get_side_bar_label("./src/assets/icons/folder-icon-blue.svg", "folder_icon")
        
        side_bar_layout.addWidget(folder_label)
        
        self.side_bar.setLayout(side_bar_layout)
        
        body.addWidget(self.side_bar)
        
        # split view
        self.hsplit = QSplitter(Qt.Orientation.Horizontal)
        
        # frame and layout to hold tree view (file manager)
        self.tree_frame = QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100, 0)
        self.tree_frame.setContentsMargins(0, 0, 0, 0)        
        
        tree_frame_layout = QHBoxLayout()
        tree_frame_layout.setSpacing(0)
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.tree_frame.setStyleSheet('''
                                      QFrame {
                                          background-color: #21252b;
                                          border-radius: 5px;
                                          border: none;
                                          padding: 5px;
                                          color: #D3D3D3;
                                      }
                                      QFrame:hover {
                                          color: white;
                                          
                                      }
                                      ''')
        
        # create file system model to show in tree view
        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        
        # File system filters
        self.model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllDirs | QDir.Filter.Files)
        
        # Tree view
        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("Arial", 13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        
        # Add custom context menu
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        
        # Handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Hide header and hide other columns except for name
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)
        
        # setup layout
        tree_frame_layout.addWidget(self.tree_view)
        self.tree_frame.setLayout(tree_frame_layout)
        
        # Tab widget to add editor to
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)
        
        # add tree view and tab view
        self.hsplit.addWidget(self.tree_frame)
        self.hsplit.addWidget(self.tab_view)
        
        
        body.addWidget(self.hsplit)
        body_frame.setLayout(body)
        
        self.setCentralWidget(body_frame)
                
    def tree_view_context_menu(self, pos):
        ...
        
    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)
        
    def close_tab(self, index):
        self.tab_view.removeTab(index)
        
    def show_hide_tab(self, e, type_):
        if self.tree_frame.isHidden():
            self.tree_frame.show()
        else:
            self.tree_frame.hide()
        
    def new_file(self):
        self.set_new_tab(None, is_new_file=True)
                        
    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()
        
        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)
        
    def save_as(self):
        editor = self.tab_view.currentWidget()
        if editor is None:
            return
        
        file_path = QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path is None:
            self.statusBar().showMessage("Canceled", 2000)
            return
        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}",2000)
        self.current_file = path
        
    def open_file(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        
        new_file = QFileDialog.getOpenFileName(self,
                                               "Pick a File", "", "All Files (*);; Python Files (*.py)",
                                               options=ops)
        if new_file == '':
            self.statusBar().showMessage("Canceled", 2000)
            return
        f = Path(new_file)
        self.set_new_tab(f)
        
    def open_folder(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        
        new_folder = QFileDialog.getExistingDirectory(self, "Pick a Folder", "", options=ops)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)
    
    def copy(self):
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()
                        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())