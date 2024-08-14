from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.Qsci import *
import keyword
import pkgutil

import ui.resouces_rc
from lexer import PyCustomLexer

class Editor(QsciScintilla):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
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
        
        # Lexer
        self.pylexer = PyCustomLexer(self)
        self.pylexer.setDefaultFont(self.window_font)
        
        # Api
        self.api = QsciAPIs(self.pylexer)
        for key in keyword.kwlist + dir(__builtins__):
            self.api.add(key)
            
        for _, name, _ in pkgutil.iter_modules():
            self.api.add(name)
                    
        self.api.prepare()
                    
        self.setLexer(self.pylexer)
        
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