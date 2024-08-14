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
from searcher import *
from ui.file_manager import FileManager

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        
        self.side_bar_clr = "#282c34"
        
        self.init_ui()
        
        self.current_file = None
        self.current_side_bar = None
        
    def init_ui(self):
        self.app_name = "TEXT EDITOR"
        self.setWindowTitle(self.app_name)
        self.resize(1300, 900)
        
        self.setStyleSheet(open("./src/css/style.qss", "r").read())
        
        self.window_font = QFont("Arial")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        
        
        self.set_up_menu()
        self.set_up_body()
        self.set_up_status_bar()
        
        self.show()
        
    def set_up_status_bar(self):
        status_bar = QStatusBar(self)
        status_bar.setStyleSheet("color: #d3d3d3;")
        status_bar.showMessage("Ready", 3000)
        self.setStatusBar(status_bar)
        
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
        
    def get_editor(self, path: Path = None, is_python_file=True) -> QsciScintilla:
        editor = Editor(self, path=path, is_python_file=is_python_file)
        return editor
    
    def is_binary(self, path):
        '''
        Check if file is binary
        '''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
    
    def set_new_tab(self, path: Path, is_new_file=False):
        if not is_new_file and self.is_binary(path):
            self.statusBar().showMessage("Cannot open binary file!", 2000)
            return
        
        if path.is_dir():
            return
        
        
        editor = self.get_editor(path, path.suffix in {".py", ".pyw"})
        
        
        if is_new_file:
            self.tab_view.addTab(editor, "Untitled")
            self.setWindowTitle("Untitled - " + self.app_name)
            self.statusBar().showMessage("Openend Untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None
            return
        
        
        # Check if file is already open
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name or self.tab_view.tabText(i) == "*" + path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return
                
        # Create new tab
        self.tab_view.addTab(editor, path.name)
        editor.setText(path.read_text(encoding="utf-8"))
        self.setWindowTitle(f"{path.name} - {self.app_name}")
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path.name}", 2000)

    def set_cursor_pointer(self, e):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def set_cursor_arrow(self, e):
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def get_side_bar_label(self, path, name):
        label = QLabel()
        label.setPixmap(QPixmap(path).scaled(QSize(30, 30)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e, name)
        label.enterEvent = self.set_cursor_pointer
        label.leaveEvent = self.set_cursor_arrow
        return label

    def get_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.NoFrame)
        frame.setFrameShadow(QFrame.Shadow.Plain)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setStyleSheet('''
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
        return frame

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
               
        
        # Tab widget to add editor to
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)
        
        # Side bar
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Shadow.Plain)
        self.side_bar.setStyleSheet(f'''
                                    background-color: {self.side_bar_clr};
                                    ''')
        side_bar_layout = QVBoxLayout()
        side_bar_layout.setContentsMargins(5,10,5,0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        
        
        # Setup labels
        folder_label = self.get_side_bar_label("./src/assets/icons/folder-icon-blue.svg", "file_manager")        
        side_bar_layout.addWidget(folder_label)
        
        search_label = self.get_side_bar_label("./src/assets/icons/search-icon.svg", "search")
        side_bar_layout.addWidget(search_label)
        
        
        self.side_bar.setLayout(side_bar_layout)
        
        # split view
        self.hsplit = QSplitter(Qt.Orientation.Horizontal)
        
        
        ## FILE MANAGER
        # frame and layout to hold tree view (file manager)
        self.file_manager_frame = self.get_frame()
        self.file_manager_frame.setMaximumWidth(400)
        self.file_manager_frame.setMinimumWidth(200) 
        
        self.file_manager_layout = QVBoxLayout()
        self.file_manager_layout.setSpacing(0)
        self.file_manager_layout.setContentsMargins(0, 0, 0, 0)
        
        self.file_manager = FileManager(
            tab_view = self.tab_view,
            set_new_tab = self.set_new_tab,
            main_window = self
            )
        
        # setup layout
        self.file_manager_layout.addWidget(self.file_manager)
        self.file_manager_frame.setLayout(self.file_manager_layout)
        self.file_manager_layout
        
        
        # Search view
        self.search_frame = self.get_frame()
        self.search_frame.setMaximumWidth(400)
        self.search_frame.setMinimumWidth(200)

        search_layout = QVBoxLayout()
        search_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        search_layout.setContentsMargins(0, 10, 0, 0)
        search_layout.setSpacing(0)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search")
        search_input.setFont(self.window_font)
        search_input.setAlignment(Qt.AlignmentFlag.AlignTop)
        search_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #21252b;
                border-radius: 5px;
                border: 1px solid #d3d3d3;
                padding: 5px;
                color: #d3d3d3;
            }
            
            QLineEdit:hover {
                color: white;
            }
            """)
        
        # Search checkboxes
        self.search_box = QCheckBox("Search in modules")
        self.search_box.setFont(self.window_font)
        self.search_box.setStyleSheet("color:white; margin-bottom: 10px;")
        
        
        self.search_worker = SearchWorker()
        self.search_worker.finished.connect(self.search_finished)
        
        search_input.textChanged.connect(
            lambda text: self.search_worker.update(
                text,
                self.model.rootDirectory().absolutePath(),
                self.search_box.isChecked()
            )
        )
        
        # Search list view
        self.search_list_view = QListWidget()
        self.search_list_view.setFont(QFont("Arial", 13))
        self.search_list_view.setStyleSheet(
            """
            QListWidget {
                background-color: #21252b;
                border-radius: 5px;
                border: 1px solid #d3d3d3;
                padding: 5px;
                color: #d3d3d3;
            }
            """)
        self.search_list_view.itemClicked.connect(self.search_list_view_clicked)
        
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_input)
        search_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))
        search_layout.addWidget(self.search_list_view)
        
        self.search_frame.setLayout(search_layout)
        
        
        # add tree view and tab view
        self.hsplit.addWidget(self.file_manager_frame)
        self.hsplit.addWidget(self.tab_view)
        
        
        body.addWidget(self.side_bar)
        body.addWidget(self.hsplit)
        body_frame.setLayout(body)
        
        self.setCentralWidget(body_frame)
        
    def search_finished(self, items):
        self.search_list_view.clear()
        for i in items:
            self.search_list_view.addItem(i)
            
    def search_list_view_clicked(self, item: SearchItem):
        self.set_new_tab(Path(item.full_path))
        editor: Editor = self.tab_view.currentWidget()
        editor.setCursorPosition(item.line_n, item.end)
        editor.setFocus()
    
    def show_dialog(self, title, msg) -> int:
        dialog = QMessageBox(self)
        dialog.setFont(self.font())
        dialog.font().setPointSize(14)
        dialog.setWindowTitle(title)
        dialog.setWindowIcon(QIcon(":/assets/icons/close-icon.svg"))
        dialog.setText(msg)
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QMessageBox.StandardButton.No)
        dialog.setIcon(QMessageBox.Icon.Warning)
        return dialog.exec_()
                
    def tree_view_context_menu(self, pos):
        ...
          
    def close_tab(self, index):
        editor: Editor = self.tab_view.currentWidget()
        if editor.current_file_changed:
            dialog = self.show_dialog(
                "Close", f"Do you want to save the changes made to {self.current_file.name}?"
            )
            if dialog == QMessageBox.StandardButton.Yes:
                self.save_file()
        
        self.tab_view.removeTab(index)
        
    def show_hide_tab(self, e, type_):
        if type_ == "file_manager":
            if not (self.file_manager_frame in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.file_manager_frame)
        elif type_ == "search":
            if not (self.search_frame in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.search_frame)
        
        if self.current_side_bar == type_:
            frame = self.hsplit.children()[0]
            if frame.isHidden():
                frame.show()
            else:
                frame.hide()
        
        self.current_side_bar = type_
        
    def new_file(self):
        self.set_new_tab(Path("Untitled"), is_new_file=True)
                        
    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()
        
        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)
        editor.current_file_changed = False
        
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
        editor.current_file_changed = False
        
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