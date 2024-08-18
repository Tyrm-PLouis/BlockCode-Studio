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
from ui.menu import Menu
import ui.resouces_rc
import project


class PathField(QWidget):
    def __init__(self, name: str):
        super().__init__()
        button = QPushButton("Browse")
        button.clicked.connect(self.open)
        self.field = QLineEdit()
        
        layout = QHBoxLayout()
        layout.addWidget(self.field)
        layout.addWidget(button)
        
        field_layout = QFormLayout(self)
        field_layout.addRow(name, layout)
        
    def open(self):
        name = QFileDialog.getExistingDirectory(self, "Select Directory")
        if name:
            self.field.setText(name)

class WelcomeWindow(QWidget):
    def __init__(self, stackedWidget : QStackedWidget, editor_win) -> None:
        super(QWidget, self).__init__()
        
        self.stackedWidget = stackedWidget
        self.editorWindow = editor_win
        
        self.init_ui()
        
    def init_ui(self):
        
        self.resize(1300, 900)
        self.setAutoFillBackground(True)
        self.setStyleSheet(open("./src/css/style.qss", "r").read())
        self.window_font = QFont("Arial")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        self.btn_font = QFont("Silkscreen", 14)
        
        #       -------------------------------
        #       --------- TITLE ICON ----------
        #region -------------------------------
        self.title_icon = QPixmap("./src/assets/title_icon.png")
        #endregion
        
        #       -------------------------------
        #       -------- TITLE LABEL ----------
        #region -------------------------------
        self.title_label = QLabel("Datapack Editor")
        self.title_label.setFont(QFont("Silkscreen", 16))
        self.title_label.setPixmap(self.title_icon)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #endregion
        
        #       -------------------------------
        #       ----- OPEN EDITOR BUTTON ------
        #region -------------------------------
        self.open_editor = QPushButton("Open editor")
        self.open_editor.setFont(self.btn_font)
        self.open_editor.setFixedSize(396, 36)
        self.open_editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #endregion
        
        #       -------------------------------
        #       ---- CREATE PROJECT BUTTON ----
        #region -------------------------------        
        self.create_project_button = QPushButton("Create New Project")
        self.create_project_button.setFont(self.btn_font)
        self.create_project_button.setFixedSize(396, 36)
        self.create_project_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #endregion
        
        #       -------------------------------
        #       ----- OPEN PROJECT BUTTON -----
        #region -------------------------------
        self.open_project_button = QPushButton("Open Project")
        self.open_project_button.setFont(self.btn_font)
        self.open_project_button.setFixedSize(396, 36)
        self.open_project_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #endregion
        
        #       -------------------------------
        #       ---- BUTTONS CLICK CONNECT ----
        #region -------------------------------
        self.open_editor.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.editorWindow))
        self.create_project_button.clicked.connect(self.create_project)
        self.open_project_button.clicked.connect(self.open_project) 
        #endregion
        
        #       -------------------------------
        #       -------- LAYOUTS INIT ---------
        #region -------------------------------
        self.main_layout = QVBoxLayout()
        self.center_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        #endregion
        
        #       -------------------------------
        #       ------- BUTTON LAYOUT ---------
        #region -------------------------------
        self.button_layout.setSpacing(20)
        self.button_layout.addWidget(self.open_editor)
        self.button_layout.addWidget(self.create_project_button)
        self.button_layout.addWidget(self.open_project_button)
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #endregion
        
        #       -------------------------------
        #       ------- CENTER LAYOUT ---------
        #region -------------------------------
        self.center_layout.addLayout(self.button_layout)
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #endregion
        
        #       -------------------------------
        #       -------- MAIN LAYOUT ----------
        #region -------------------------------
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.center_layout)
        self.main_layout.addWidget(self.set_up_status_bar())
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        #endregion
        
        self.setLayout(self.main_layout)

    def set_up_status_bar(self) -> QStatusBar:
        status_bar = QStatusBar(self)
        status_bar.setStyleSheet("color: #d3d3d3;")
        status_bar.showMessage("Ready", 3000)
        return status_bar

    def create_project(self):
        """
        Ask user for a project name, and some options (like a resource pack path)
        Ask for path for project (datapack)
        Generate all files needed
        """
        create_project_dialog = QDialog(self)
        create_project_dialog.setWindowTitle("Creating a new project")
        
        dp_path_field = PathField("Datapack folder*")
        rp_path_field = PathField("Resource pack folder")
        
        next_button = QPushButton("Next")
        next_button.setFixedSize(150, 36)
        next_button.setDefault(True)
        next_button.setEnabled(False)
        
        abort_button = QPushButton("Abort")
        abort_button.setFixedSize(150, 36)
        
        buttons = QDialogButtonBox(self)
        
        buttons.addButton(next_button, QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(abort_button, QDialogButtonBox.ButtonRole.RejectRole)
        
        buttons.accepted.connect(create_project_dialog.accept)
        buttons.rejected.connect(create_project_dialog.reject)
        buttons.setCenterButtons(True)
        
        project_name_field = QLineEdit() 
        project_name_field_layout = QFormLayout(self)
        project_name_field_layout.addRow("Datapack name (*):   ", project_name_field)
        
        project_name_field.textChanged.connect(lambda: self.on_text_changed(next_button, project_name_field, dp_path_field.field))
        dp_path_field.field.textChanged.connect(lambda: self.on_text_changed(next_button, dp_path_field.field, project_name_field))
        
        namespace_name_field = QLineEdit()
        namespace_name_field.setPlaceholderText("(leave blank to use datapack's name)")
        namespace_name_field_layout = QFormLayout(self)
        namespace_name_field_layout.addRow("Datapack namespace:", namespace_name_field)
        
        p_layout = QVBoxLayout()
        p_layout.addLayout(project_name_field_layout)
        p_layout.addLayout(namespace_name_field_layout)
        p_layout.addWidget(dp_path_field)
        p_layout.addWidget(rp_path_field)
        p_layout.addWidget(buttons)
        p_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        create_project_dialog.setLayout(p_layout)
        
        
        create_project_dialog.open()
        
        create_project_dialog.accepted.connect(lambda: self.action_next(namespace_name_field, project_name_field, dp_path_field, rp_path_field))
        create_project_dialog.rejected.connect(lambda: print("ABORT"))
        
        # if create_project_dialog.exec_():
        #     print("NEXT")
        #     if namespace_name_field.text():
        #         project.namespace = namespace_name_field.text()
        #     else:
        #         project.namespace = project_name_field.text()
        #     print(project.namespace)
        #     project.printDir(f"{dp_path_field.field.text()}/{project_name_field.text()}", project.namespaces)
            
        #     if rp_path_field.field.text() != '':
        #         ...
        #         # if namespace_name_field.text:
        #         #     project.namespace = namespace_name_field.text
        #         # else:
        #         #     project.namespace = project_name_field.text
            
        # else:
        #     print("ABORT")
    
    def on_text_changed(self, btn: QPushButton, l1: QLineEdit, l2: QLineEdit):
        btn.setEnabled(bool(l1.text()) and bool(l2.text()))
    
    def action_next(self, namespace_name_field, project_name_field, dp_path_field, rp_path_field):
            pr_name = project_name_field.text()
            namespace = namespace_name_field.text()
            
            print(f"[{pr_name}] | [{namespace}]")
            
            name = pr_name
            if namespace:
                name = namespace
            
            pr_gen = project.ProjectGenerator(namespace if namespace else pr_name)
            
        
            print(pr_gen.namespace)
            # pr_gen.printDir(f"{dp_path_field.field.text()}/{project_name_field.text()}", pr_gen.get_namespaces())
            pr_gen.CreateDir(f"{dp_path_field.field.text()}/{project_name_field.text()}", pr_gen.get_namespaces())
            
            
            if rp_path_field.field.text() != '':
                ...
                # if namespace_name_field.text:
                #     project.namespace = namespace_name_field.text
                # else:
                #     project.namespace = project_name_field.text
        
    
    def open_project(self):
        """
        Ask user a folder to open
        If folder contain correct data (mcmeta file + data + settings.json)
        Then we load the project and if specified in settings.json, we load resource pack data (with RP toggle activated to tell 
        any DP related features that it can also modify RP)
        """
        ...
        
    def generate_project(self, name:str, namespace:str, path:str):
        ...

# FIXME : Trouver comment modifier cette classe pour pouvoir ajouter la statusBar et garder le layout du QFrame

class EditorWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        
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
        
        self.menu = Menu(self)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        self.set_up_menu()
        self.set_up_body()
        
        self.status_bar = self.set_up_status_bar()
        
        self.main_layout.addWidget(self.status_bar)
        self.setLayout(self.main_layout)

    
    def set_up_status_bar(self) -> QStatusBar:
        status_bar = QStatusBar(self)
        status_bar.setStyleSheet("color: #d3d3d3;")
        status_bar.showMessage("Ready", 3000)
        return status_bar
        
    def set_up_menu(self):
        menu_bar = QMenuBar(self)
        menu_bar.addMenu(self.menu.FILE_MENU)
        menu_bar.addMenu(self.menu.EDIT_MENU)
        self.main_layout.addWidget(menu_bar)
                
    def get_editor(self, path: Path = None, file_type: str = "") -> QsciScintilla:
        editor = Editor(self, path=path, file_ext=file_type)
        return editor
    
    def is_binary(self, path):
        '''
        Check if file is binary
        '''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)
    
    def set_new_tab(self, path: Path, is_new_file=False):
        if not is_new_file and self.is_binary(path):
            self.status_bar.showMessage("Cannot open binary file!", 2000)
            return
        
        if path.is_dir():
            return
        
        
        editor = self.get_editor(path, path.suffix)
        
        
        if is_new_file:
            self.tab_view.addTab(editor, "Untitled")
            self.setWindowTitle("Untitled - " + self.app_name)
            self.status_bar.showMessage("Openend Untitled")
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
        self.status_bar.showMessage(f"Opened {path.name}", 2000)

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
        
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.main_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.main_frame.setLineWidth(0)
        self.main_frame.setMidLineWidth(0)
        self.main_frame.setContentsMargins(0,0,0,0)
        self.main_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        body = QHBoxLayout()
        body.setContentsMargins(0,0,0,0)
        body.setSpacing(0)
        
        self.main_frame.setLayout(body)
               
        
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
        self.main_frame.setLayout(body)
        
        self.main_layout.addWidget(self.main_frame)
        
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
                                

if __name__ == '__main__':
    app = QApplication([])
    
    
    app_name = "BlockCode Studio"
    app.setApplicationName(app_name)
    
    app.setWindowIcon(QIcon("./src/assets/DatapackEditorLogo.png"))
    
    stackedWidget = QStackedWidget()
    editor = EditorWindow()
    window = WelcomeWindow(stackedWidget, editor)
    
    stackedWidget.resize(1300, 900)
    stackedWidget.setStyleSheet('''
        background-color: #282c34;
        color: #d3d3d3;
    ''')
    stackedWidget.addWidget(window)
    stackedWidget.addWidget(editor)
    stackedWidget.setCurrentWidget(window)
    
    #window.open_editor.clicked.connect(lambda: stackedWidget.setCurrentWidget(editor))
    stackedWidget.show()
    
    sys.exit(app.exec())