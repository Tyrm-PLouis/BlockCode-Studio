import re
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
import keyword
import types
import builtins



# Créer son propre affichage syntaxique concernant un langage
class PyCustomLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(PyCustomLexer, self).__init__(parent)
        
        self.color1 = "#abb2bf"
        self.color2 = "#282c34"
        
        # Options par défaut
        self.setDefaultColor(QColor(self.color1))
        self.setDefaultPaper(QColor(self.color2))
        self.setDefaultFont(QFont("Consolas", 14))
        
        # Mots clés
        self.KEYWORD_LIST = keyword.kwlist
        
        
        self.builtin_functions_names = [name for name, obj in vars(builtins).items()
                                        if isinstance(obj, types.BuiltinFunctionType)]
        
        # Assignation des couleurs par types
        self.DEFAULT = 0
        self.KEYWORD = 1
        self.TYPES = 2
        self.STRING = 3
        self.KEYARGS = 4
        self.BRACKETS = 5
        self.COMMENTS = 6
        self.CONSTANTS = 7
        self.FUNCTIONS = 8
        self.CLASSES = 9
        self.FUNCTION_DEF = 10
        
        # Styles
        self.setColor(QColor(self.color1), self.DEFAULT)
        self.setColor(QColor("#e7379b"), self.KEYWORD)
        self.setColor(QColor("#35a1df"), self.TYPES)
        self.setColor(QColor("#b2d546"), self.STRING)
        self.setColor(QColor("#e7379b"), self.KEYARGS)
        self.setColor(QColor("#eb59c4"), self.BRACKETS)
        self.setColor(QColor("#84d1b2"), self.COMMENTS)
        self.setColor(QColor("#d8b62f"), self.CONSTANTS)
        self.setColor(QColor("#0bae13"), self.FUNCTIONS)
        self.setColor(QColor("#00702f"), self.CLASSES)
        self.setColor(QColor("#0bae13"), self.FUNCTION_DEF)
        
        # Paper color
        self.setPaper(QColor(self.color2), self.DEFAULT)
        self.setPaper(QColor(self.color2), self.KEYWORD)
        self.setPaper(QColor(self.color2), self.TYPES)
        self.setPaper(QColor(self.color2), self.STRING)
        self.setPaper(QColor(self.color2), self.KEYARGS)
        self.setPaper(QColor(self.color2), self.BRACKETS)
        self.setPaper(QColor(self.color2), self.COMMENTS)
        self.setPaper(QColor(self.color2), self.CONSTANTS)
        self.setPaper(QColor(self.color2), self.FUNCTIONS)
        self.setPaper(QColor(self.color2), self.CLASSES)
        self.setPaper(QColor(self.color2), self.FUNCTION_DEF)
        
        # Font
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.DEFAULT)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.KEYWORD)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.CLASSES)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.FUNCTION_DEF)
        
        
    def language(self) -> str:
        return "PYCustomLexer"
    
    
    def description(self, style: int) -> str:
        if style == self.DEFAULT:
            return "DEFAULT"
        elif style == self.KEYWORD:
            return "KEYWORD"
        elif style == self.TYPES:
            return "TYPES"
        elif style == self.STRING:
            return "STRING"
        elif style == self.KEYARGS:
            return "KEYARGS"
        elif style == self.BRACKETS:
            return "BRACKETS"
        elif style == self.COMMENTS:
            return "COMMENTS"
        elif style == self.CONSTANTS:
            return "CONSTANTS"
        elif style == self.FUNCTIONS:
            return "FUNCTIONS"
        elif style == self.CLASSES:
            return "CLASSES"
        elif style == self.FUNCTION_DEF:
            return "FUNCTION_DEF"
        else:
            return ""
        
    def get_tokens(self, text) -> list[str, int]:
        # Tokeniser le texte
        # ------------------
        p = re.compile(r'[*]\/|\/[*]|\s+|\w+|\W')
        
        # la liste de jetons est une liste de tuples (nom du jeton, taille du jeton)
        return [ (token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]
        
    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)
        editor: QsciScintilla = self.parent()
        
        text = editor.text()[start:end]
        # print(text)
        tokens = self.get_tokens(text)
        
        string_flag = False
        comment_flag = False
        
        if start > 0:
            previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style == self.STRING:
                string_flag = False
            if previous_style == self.COMMENTS:
                comment_flag = False
        
        def next_token(skip: int=None):
            if len(tokens) > 0:
                if skip is not None and skip != 0:
                    for _ in range(skip - 1):
                        if len(tokens) > 0:
                            tokens.pop(0)
                return tokens.pop(0)
            else:
                return None
            
        def peek_token(n = 0):
            try:
                return tokens[n]
            except IndexError:
                return ['']
            
        def skip_space_peek(skip=None):
            i = 0
            token = (' ')
            if skip is not None:
                i = skip
            while token[0].isspace():
                token = peek_token(i)
                i += 1
            return token, i
        
        while True:
            current_token = next_token()
            if current_token is None:
                break
            token: str = current_token[0]
            token_length = current_token[1]
            
            if comment_flag:
                self.setStyling(token_length, self.COMMENTS)
                if token.startswith("\n"):
                    comment_flag = False
                continue
            
            
            if string_flag:
                self.setStyling(token_length, self.STRING)
                if token == '"' or token == "'":
                    string_flag = False
                continue
            
            if token == "class":
                name, ni = skip_space_peek()
                brac_or_colon, _ = skip_space_peek(ni)
                if name[0].isidentifier() and brac_or_colon[0] in (":", "("):
                    self.setStyling(token_length, self.KEYWORD)
                    _ = next_token(ni)
                    self.setStyling(name[1] + 1, self.CLASSES)
                    continue
                else:
                    self.setStyling(token_length, self.KEYWORD)
                    continue
            elif token == "def":
                name, ni = skip_space_peek()
                if name[0].isidentifier():
                    self.setStyling(token_length, self.KEYWORD)
                    _ = next_token(ni)
                    self.setStyling(name[1]+1, self.FUNCTION_DEF)
                    continue
                else:
                    self.setStyling(token_length, self.KEYWORD)
                    continue
            elif token in self.KEYWORD_LIST:
                self.setStyling(token_length, self.KEYWORD)
            elif token.isnumeric() or token == 'self':
                self.setStyling(token_length, self.CONSTANTS)
            elif token in ["(",")","{","}","[","]"]:
                self.setStyling(token_length, self.BRACKETS)
            elif token == '"' or token == "'":
                self.setStyling(token_length, self.STRING)
                string_flag = True
            elif token == "#":
                self.setStyling(token_length, self.COMMENTS)
                comment_flag = True
            elif token in self.builtin_functions_names or token in ['+', '-', '*', '/', '%', '=', '<', '>']:
                self.setStyling(token_length, self.TYPES)
            else:
                self.setStyling(token_length, self.DEFAULT)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        