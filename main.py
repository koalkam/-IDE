from re import compile
from sys import exit

from PyQt5.Qsci import QsciScintilla as Scintilla, QsciLexerCustom as CustomLexer, QsciLexerPython
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow

# variables
INITIAL_WINDOW_WIDTH = 1300
INITIAL_WINDOW_HEIGHT = 700
colors = {'bg': '#3c3f41', 'editor-bg': '#2b2b2b', 'default-text': '#a9b7c6'}

KEYWORDS = ['import', 'from', 'def', 'class', 'with', 'as']


# Syntax Highlight class
class SyntaxHighlighter(CustomLexer):
    def __init__(self):
        super(SyntaxHighlighter, self).__init__()
        self.STYLES = {
            'default': 0,
            'keyword': 1,
            'builtin': 3,
            'string': 5,
            'int': 6,
            'self': 7,
            'function': 8,
            'special': 9
        }

        self.setDefaultPaper(QColor(colors['editor-bg']))
        self.setDefaultColor(QColor(colors['default-text']))

        self.setColor(QColor(colors['default-text']), self.STYLES['default'])
        self.setPaper(QColor(colors['editor-bg']), self.STYLES['default'])

    def description(self, style: int) -> str:
        pass

    def language(self) -> str:
        return 'python'

    def styleText(self, start: int, end: int) -> None:
        print('styling-lol')
        self.startStyling(start)

        text = self.parent().text()[start:end]
        print(text)

        # tokenizing text using regex
        tokenizer = compile('\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W')
        tokens = [(token, len(token)) for token in tokenizer.findall(text)]
        print(tokens)
        for token in tokens:
            self.setStyling(token[1], 100)

# main window class
class IDE(QMainWindow):
    def __init__(self):
        super(IDE, self).__init__()

        self.setGeometry(0, 0, INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT)
        self.setStyleSheet(f'background-color: {colors["bg"]}; border: flat;')

        self.editor = Scintilla(self)
        self.editor.resize(self.width() - 100, self.height() - 100)

        self.editor.setLexer(SyntaxHighlighter())

        self.show()


# running the app
app = QApplication([])
window = IDE()
exit(app.exec())
