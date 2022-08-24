from re import compile
from sys import exit

from PyQt5.Qsci import QsciScintilla as Scintilla, QsciLexerCustom as CustomLexer, QsciAPIs
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow

# variables
INITIAL_WINDOW_WIDTH = 1300
INITIAL_WINDOW_HEIGHT = 700
colors = {'main-bg': '#3c3f41',
          'default-bg': '#2b2b2b', 'default-text': '#a9b7c6',
          'keyword-text': '#cc7832', 'keyword-bg': '#2b2b2b',
          'builtin-text': '#8888c6', 'builtin-bg': '#2b2b2b',
          'comment-text': '#808080', 'comment-bg': '#2b2b2b',
          'int-text': '#6294ba', 'int-bg': '#2b2b2b',
          'self-text': '#94558d', 'self-bg': '#2b2b2b',
          'function-text': '#ffc66d', 'function-bg': '#2b2b2b',
          'special-text': '#b200b2', 'special-bg': '#2b2b2b'}

KEYWORDS = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
            'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
            'in', 'is', 'lambda', 'not', 'or', 'pass', 'return', 'try',
            'while', 'with', 'yield']

BUILTINS = ['print', 'len', 'range', 'int', 'str', 'bool', 'list', 'set', 'map']


func_name_next = False
string_color_mode = False
comment_color_mode = False


# Syntax Highlight class
class SyntaxHighlighter(CustomLexer):
    def __init__(self):
        super(SyntaxHighlighter, self).__init__()
        self.STYLES = {
            'default': 0,
            'keyword': 1,
            'builtin': 3,
            'comment': 4,
            # 'string': 5,
            'int': 6,
            'self': 7,
            'function': 8,
            'special': 9
        }

        self.setDefaultPaper(QColor(colors['default-bg']))
        self.setDefaultColor(QColor(colors['default-text']))

        for item in self.STYLES.keys():
            self.setColor(QColor(colors[f'{item}-text']), self.STYLES[item])
            self.setPaper(QColor(colors[f'{item}-bg']), self.STYLES[item])

    def description(self, style: int) -> str:
        return 'idk'

    def language(self) -> str:
        return 'python'


    def styleText(self, start: int, end: int) -> None:
        global func_name_next
        global string_color_mode
        global comment_color_mode

        self.startStyling(start)

        text = self.parent().text()[start:end]

        # tokenizing text using regex
        tokenizer = compile(r'\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W')
        tokens = [(token, len(token)) for token in tokenizer.findall(text)]

        # coloring tokens
        for token in tokens:
            if token[0] in KEYWORDS:
                self.setStyling(token[1], 1)
                if token[0] == 'def':
                    func_name_next = True

            elif token[0] in BUILTINS:
                self.setStyling(token[1], 3)
            elif token[0] == 'self':
                self.setStyling(token[1], 7)
            elif token[0].startswith('__'):
                self.setStyling(token[1], 9)
                func_name_next = False
            elif token[0].isdigit() and not string_color_mode:
                self.setStyling(token[1], 6)
            elif func_name_next and token[0] != ' ':
                func_name_next = False
                self.setStyling(token[1], 8)
            elif token[0] == '#' and string_color_mode == False:
                comment_color_mode = True
                self.setStyling(token[1], 4)
            # elif comment_color_mode:
            #     self.setStyling(token[1], 4)
            else:
                self.setStyling(token[1], 0)


# main window class
class IDE(QMainWindow):
    def __init__(self):
        super(IDE, self).__init__()

        self.setGeometry(0, 0, INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT)
        self.setStyleSheet(f'background-color: {colors["main-bg"]}; border: flat;')

        self.editor = Scintilla(self)
        self.editor.resize(self.width() - 100, self.height() - 100)
        self.lexer = SyntaxHighlighter()

        self.editor.setLexer(self.lexer)
        self.lexer.setParent(self.editor)
        api = QsciAPIs(self.lexer)

        self.show()


# running the app
app = QApplication([])
window = IDE()
exit(app.exec())
