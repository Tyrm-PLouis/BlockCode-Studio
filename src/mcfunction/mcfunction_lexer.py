import re
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciLexerCustom, QsciScintilla

from . import mcfunction


class McFunctionLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(McFunctionLexer, self).__init__(parent)
        
        self.background_color       = QColor("#2c313c")
        self.default_text_color     = QColor("#9a9a9a")
        self.default_font           = QFont("Consolas", 14)
        self.default_font_bold      = QFont("Consolas", 14, weight = QFont.Weight.Bold)
        
        self.command_color          = QColor("#23a9ed")
        self.sub_command_color      = QColor("#407cb8")
        self.selector_color         = QColor("#ffe851")
        self.string_color           = QColor("#2fd74e")
        self.comment_color          = QColor("#889da2")
        self.comment_title_color    = QColor("#dbb700")
        self.attribute_color        = QColor("#7459ed")
        self.namespace_color        = QColor("#ea4470")
        self.resource_color         = QColor("#c11353")
        self.brackets_color         = QColor("#b40cde")
        self.values_color           = QColor("#31c193")
        self.keyword_color          = QColor("#00e463")
        
        # ---------------------
        # Default text settings
        # ---------------------
        self.setDefaultColor(self.default_text_color)
        self.setDefaultPaper(self.background_color)
        self.setDefaultFont(self.default_font)
        
        # ---------------------------
        # Initialize colors per style
        # ---------------------------
        self.setColor(self.command_color, mcfunction.COMMAND)
        self.setColor(self.sub_command_color, mcfunction.SUB_COMMAND)
        self.setColor(self.selector_color, mcfunction.SELECTOR)
        self.setColor(self.string_color, mcfunction.STRING)
        self.setColor(self.command_color, mcfunction.COMMENT)
        self.setColor(self.comment_title_color, mcfunction.COMMENT_TITLE)
        self.setColor(self.attribute_color, mcfunction.ATTRIBUTE)
        self.setColor(self.namespace_color, mcfunction.NAMESPACE)
        self.setColor(self.resource_color, mcfunction.RESOURCE)
        self.setColor(self.brackets_color, mcfunction.BRACKETS)
        self.setColor(self.default_text_color, mcfunction.DEFAULT)
        self.setColor(self.values_color, mcfunction.VALUES)
        self.setColor(self.keyword_color, mcfunction.KEYWORDS)
        
        # ---------------------------------
        # Initialize paper colors per style
        # ---------------------------------
        self.setPaper(self.background_color, mcfunction.COMMAND)
        self.setPaper(self.background_color, mcfunction.SUB_COMMAND)
        self.setPaper(self.background_color, mcfunction.SELECTOR)
        self.setPaper(self.background_color, mcfunction.STRING)
        self.setPaper(self.background_color, mcfunction.COMMENT)
        self.setPaper(self.background_color, mcfunction.COMMENT_TITLE)
        self.setPaper(self.background_color, mcfunction.ATTRIBUTE)
        self.setPaper(self.background_color, mcfunction.NAMESPACE)
        self.setPaper(self.background_color, mcfunction.RESOURCE)
        self.setPaper(self.background_color, mcfunction.BRACKETS)
        self.setPaper(self.background_color, mcfunction.DEFAULT)
        self.setPaper(self.background_color, mcfunction.VALUES)
        self.setPaper(self.background_color, mcfunction.KEYWORDS)
        
        # --------------------------
        # Initialize fonts per style
        # --------------------------
        self.setFont(self.default_font_bold, mcfunction.COMMAND)
        self.setFont(self.default_font, mcfunction.SUB_COMMAND)
        self.setFont(self.default_font_bold, mcfunction.SELECTOR)
        self.setFont(self.default_font, mcfunction.STRING)
        self.setFont(self.default_font, mcfunction.COMMENT)
        self.setFont(self.default_font_bold, mcfunction.COMMENT_TITLE)
        self.setFont(self.default_font, mcfunction.ATTRIBUTE)
        self.setFont(self.default_font, mcfunction.NAMESPACE)
        self.setFont(self.default_font, mcfunction.RESOURCE)
        self.setFont(self.default_font, mcfunction.BRACKETS)
        self.setFont(self.default_font, mcfunction.DEFAULT)
        self.setFont(self.default_font, mcfunction.VALUES)
        self.setFont(self.default_font, mcfunction.KEYWORDS)
        
        
        
    def language(self) -> str:
        return "mcfunction"
    
    def description(self, style: int) -> str:
        if style == mcfunction.COMMAND:
            return "COMMAND"
        elif style == mcfunction.SUB_COMMAND:
            return "SUB_COMMAND"
        elif style == mcfunction.SELECTOR:
            return "SELECTOR"
        elif style == mcfunction.STRING:
            return "STRING"
        elif style == mcfunction.COMMENT:
            return "COMMENT"
        elif style == mcfunction.COMMENT_TITLE:
            return "COMMENT_TITLE"
        elif style == mcfunction.ATTRIBUTE:
            return "ATTRIBUTE"
        elif style == mcfunction.NAMESPACE:
            return "NAMESPACE"
        elif style == mcfunction.RESOURCE:
            return "RESOURCE"
        elif style == mcfunction.BRACKETS:
            return "BRACKETS"
        elif style == mcfunction.DEFAULT:
            return "DEFAULT"
        elif style == mcfunction.VALUES:
            return "VALUES"
        elif style == mcfunction.KEYWORDS:
            return "KEYWORDS"
        else:
            return ""
    
    def styleText(self, start: int, end: int) -> None:
        # --------------
        # Flags and vars
        # --------------
        sub_command_flag    = False     # True when we are in an execute command
        string_flag         = False     # True if token is in string
        comment_flag        = False     # True if token is in comment line
        comment_title_flag  = False     # True if token is in a line with more than one # ("##, ###...")
        namespace_flag      = False     # True if we are in a namespace --> toggles resource styling
        keyword_flag        = False     # True if we are in [] or {} when adding nbt search
        bracket_count       = 0         # Count brackets when we are in keyword flag
        
        # ----------------------------
        # Initialize styling procedure
        # ----------------------------
        self.startStyling(start)
        editor: QsciScintilla = self.parent()
            
        # ------------------------
        # Get text shown at screen
        # ------------------------
        text = editor.text()[start:end]
        
        # --------------------------
        # Get the tokens in the text
        # --------------------------
        pattern = re.compile(r"[*]\/|\/[*]|@[a-z]|##|\s+|\w+|\W")
        
        tokens : list[str, int] = [ (token, len(bytearray(token, "utf-8"))) for token in pattern.findall(text)]
        
        # --------------
        # Style the text
        # --------------
                
        if start > 0:
            previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style == mcfunction.STRING:
                string_flag = False
            if previous_style == mcfunction.COMMENT:
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
            
        def get_next_token():
            if len(tokens) > 0:
                return tokens[0]
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
            token_len = current_token[1]
            
            nxt_token = get_next_token()
            
            if token.startswith("\n") or token.startswith("\r"):
                string_flag = False
                comment_flag = False
                keyword_flag = False
                namespace_flag = False
                sub_command_flag = False
                comment_title_flag = False
                continue
            
            
            if nxt_token is not None:
                token_nxt = nxt_token[0]
                token_len_nxt = nxt_token[1]
            
            
            if comment_flag:
                self.setStyling(token_len, mcfunction.COMMENT)
                if token.startswith("\n"):
                    comment_flag = False
                continue
            
            if comment_title_flag:
                self.setStyling(token_len, mcfunction.COMMENT_TITLE)
                if token.startswith("\n"):
                    comment_title_flag = False
                continue
            
            
            if namespace_flag:
                if (token.isspace() or 
                    token == mcfunction.Operators.COMMA or
                    token == mcfunction.Operators.EQUAL):
                    self.setStyling(token_len, mcfunction.COMMAND)
                    namespace_flag = False
                elif token in mcfunction.T_BRACKETS:
                    self.setStyling(token_len, mcfunction.BRACKETS)
                    namespace_flag = False
                elif token == mcfunction.Operators.SLASH:
                    self.setStyling(token_len, mcfunction.COMMAND)
                else:
                    self.setStyling(token_len, mcfunction.RESOURCE)
                
                continue
            
            
            if nxt_token is not None:
                if token_nxt == mcfunction.Operators.COLON:
                    self.setStyling(token_len, mcfunction.NAMESPACE)
                    namespace_flag = True
                    continue
                
            if keyword_flag:
                if token in mcfunction.T_KEYWORDS:
                    self.setStyling(token_len, mcfunction.KEYWORDS)
                if token in mcfunction.T_OPENING_BRACKETS:
                    self.setStyling(token_len, mcfunction.BRACKETS)
                    bracket_count += 1
                if token in mcfunction.T_CLOSING_BRACKETS:
                    self.setStyling(token_len, mcfunction.BRACKETS)
                    if bracket_count > 0:
                        bracket_count -= 1
                    else:
                        keyword_flag = False
                continue
                
            if string_flag:
                self.setStyling(token_len, mcfunction.STRING)
                if token == '"' or token == "'":
                    string_flag = False
                continue
            
            # FIXME need to understand why execute command is not styling correctly
            
            if sub_command_flag:
                if token in mcfunction.T_SUBCOMMANDS:
                    self.setStyling(token_len, mcfunction.SUB_COMMAND)
                elif token in mcfunction.T_SELECTORS:
                    self.setStyling(token_len, mcfunction.SELECTOR)
                elif token.startswith("\n"):
                    sub_command_flag = False
                elif token in mcfunction.T_COMMANDS or token in mcfunction.T_OPERATORS:
                    self.setStyling(token_len, mcfunction.COMMAND)
                elif token in mcfunction.T_BRACKETS:
                    self.setStyling(token_len, mcfunction.BRACKETS)
                elif token.isnumeric():
                    self.setStyling(token_len, mcfunction.VALUES)
                elif token == '"' or token == "'":
                    self.setStyling(token_len, mcfunction.STRING)
                    string_flag = True
                elif token == "#":
                    self.setStyling(token_len, mcfunction.COMMENT)
                    comment_flag = True
                else:
                    self.setStyling(token_len, mcfunction.DEFAULT)
                continue
                
            if token in mcfunction.T_COMMANDS or token in mcfunction.T_OPERATORS:
                if token == mcfunction.Commands.EXECUTE:
                    sub_command_flag = True;
                self.setStyling(token_len, mcfunction.COMMAND)
            elif token in mcfunction.T_BRACKETS:
                self.setStyling(token_len, mcfunction.BRACKETS)
                keyword_flag = True
            elif token in mcfunction.T_KEYWORDS:
                self.setStyling(token_len, mcfunction.KEYWORDS)
            elif token in mcfunction.T_SELECTORS:
                self.setStyling(token_len, mcfunction.SELECTOR)
            elif token in mcfunction.T_SUBCOMMANDS:
                self.setStyling(token_len, mcfunction.SUB_COMMAND)
            elif token.isnumeric():
                self.setStyling(token_len, mcfunction.VALUES)
            elif token == '"' or token == "'":
                self.setStyling(token_len, mcfunction.STRING)
                string_flag = True
            elif token == "#":
                self.setStyling(token_len, mcfunction.COMMENT)
                comment_flag = True
            elif token == "##":
                self.setStyling(token_len, mcfunction.COMMENT_TITLE)
                comment_title_flag = True
            else:
                self.setStyling(token_len, mcfunction.DEFAULT)