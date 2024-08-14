from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *
import keyword
import pkgutil
from pathlib import Path

import ui.resouces_rc
from lexer import PyCustomLexer
from autocompleter import AutoCompleter

class Editor(QsciScintilla):
    def __init__(self, parent=None, path: Path = None, is_python_file = True):
        super(Editor, self).__init__(parent)
        self.path = path
        self.full_path = self.path.absolute()
        self.is_python_file = is_python_file
        
        self.cursorPositionChanged.connect(self._cursorPositionChanged)
        
        # Encoding
        self.setUtf8(True)
        # Font
        self.window_font = QFont("Arial")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)
        
        # Brace matching
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)        
        
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
        
        
        
        if self.is_python_file:
            # Lexer
            self.pylexer = PyCustomLexer(self)
            self.pylexer.setDefaultFont(self.window_font)
            
            self._api = QsciAPIs(self.pylexer)
            
            self.auto_completer = AutoCompleter(self.full_path, self._api)
            self.auto_completer.finished.connect(self.loaded_autocomplete)
            
            self.setLexer(self.pylexer)
        else:
            self.setPaper(QColor("#282c34"))
            self.setColor(QColor("#282c34"))
        
        # Line numbers
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)
        
        # Key press
        # self.keyPressEvent = self.handle_editor_press
        
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.key() == Qt.Key_Space:
            self.autoCompleteFromAll()
        else:
            return super().keyPressEvent(e)
        
    def _cursorPositionChanged(self, line: int, index: int) -> None:
        if self.is_python_file:
            self.auto_completer.get_completions(line + 1, index, self.text())        
        
    def loaded_autocomplete(self):
        ...