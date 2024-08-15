import re
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciLexerCustom, QsciScintilla



class McFunctionLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(McFunctionLexer, self).__init__(parent)