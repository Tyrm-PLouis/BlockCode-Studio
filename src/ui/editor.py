from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *
import keyword
import pkgutil
from pathlib import Path

import sys

sys.path.append("..")

import ui.resouces_rc
from lexer import PyCustomLexer
from mcfunction.mcfunction_lexer import McFunctionLexer
from autocompleter import AutoCompleter

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import EditorWindow

class Editor(QsciScintilla):
    def __init__(self, main_window, parent=None, path: Path = None, file_ext: str = ""):
        super(Editor, self).__init__(parent)
        
        self.main_window: EditorWindow = main_window
        self._current_file_changed = False
        self.first_launch = True
        
        self.path = path
        self.full_path = self.path.absolute()
        self.file_ext = file_ext
        
        self.cursorPositionChanged.connect(self._cursorPositionChanged)
        self.textChanged.connect(self._textChanged)
        
        # Encoding
        self.setUtf8(True)
        # Font
        self.window_font = QFont("Arial")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        
        # Brace matching
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#5e5f61"))
        
        
        # Indentation
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)
        
        # Autocomplete
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionThreshold(1) # Show after 1 character
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AutoCompletionUseSingle.AcusNever)

        # Caret
        self.setCaretForegroundColor(QColor("#dedcdc"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setCaretLineBackgroundColor(QColor("#2c313c"))
        
        # EOL
        self.setEolMode(QsciScintilla.EolMode.EolWindows)
        self.setEolVisibility(False)
        
        if self.file_ext == ".mcfunction":
            self.mclexer = McFunctionLexer(self)
            self.mclexer.setDefaultFont(self.window_font)
            
            self._api = QsciAPIs(self.mclexer)

            self.setLexer(self.mclexer)
        
        elif self.file_ext in {".py", ".pyw"}:
            # Lexer
            self.pylexer = PyCustomLexer(self)
            self.pylexer.setDefaultFont(self.window_font)
            
            self._api = QsciAPIs(self.pylexer)
            
            self.auto_completer = AutoCompleter(self.full_path, self._api)
            self.auto_completer.finished.connect(self.loaded_autocomplete)
            
            self.setLexer(self.pylexer)
        else:
            self.setPaper(QColor("#282c34"))
            self.setColor(QColor("#ffffff"))
        
        # Line numbers
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)
        
        # Key press
        # self.keyPressEvent = self.handle_editor_press
    
    @property
    def current_file_changed(self):
        return self._current_file_changed

    @current_file_changed.setter
    def current_file_changed(self, value: bool):
        current_index = self.main_window.tab_view.currentIndex()
        if value:
            self.main_window.tab_view.setTabText(current_index, "*"+self.path.name)
            self.main_window.setWindowTitle(f"*{self.path.name} - {self.main_window.app_name}")
        else:
            if self.main_window.tab_view.tabText(current_index).startswith("*"):
                self.main_window.tab_view.setTabText(
                    current_index,
                    self.main_window.tab_view.tabText(current_index)[1:]
                )
                self.main_window.setWindowTitle(self.main_window.windowTitle()[1:])
                
        self._current_file_changed = value

    def toggle_comment(self, text: str):
        lines = text.split('\n')
        toggled_lines = []
        for line in lines:
            if line.startswith('#'):
                toggled_lines.append(line[1:].lstrip())
            else:
                toggled_lines.append("# " + line)
        return '\n'.join(toggled_lines)
        
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.key() == Qt.Key_Space: # Ctrl + Space
            if self.is_python_file:
                pos = self.getCursorPosition()
                self.auto_completer.get_completions(pos[0]+1, pos[1], self.text())
                self.autoCompleteFromAPIs()
                return
        
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.key() == Qt.Key.Key_X: # Ctrl + X
            if not self.hasSelectedText():
                line, index = self.getCursorPosition()
                self.setSelection(line, 0, line, self.lineLength(line))
                self.cut()
                return
        
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.text() == "/": # Ctrl + /
            if self.hasSelectedText():
                start, srow, end, erow = self.getSelection()
                self.setSelection(start, 0, end, self.lineLength(end)-1)
                self.replaceSelectedText(self.toggle_comment(self.selectedText()))
                self.setSelection(start, srow, end, erow)
            else:
                line, _ = self.getCursorPosition()
                self.setSelection(line, 0, line, self.lineLength(line)-1)
                self.replaceSelectedText(self.toggle_comment(self.selectedText()))
                self.setSelection(-1, -1, -1, -1) # reset selection
                
            return
        
        return super().keyPressEvent(e)
        
    def _cursorPositionChanged(self, line: int, index: int) -> None:
        if self.file_ext in {".py", ".pyw"}:
            self.auto_completer.get_completions(line + 1, index, self.text())        
        
    def loaded_autocomplete(self):
        ...
        
    def _textChanged(self):
        if not self.current_file_changed and not self.first_launch:
            self.current_file_changed = True
            
        if self.first_launch:
            self.first_launch = False