from re import compile
from sys import exit
from PyQt5.Qsci import QsciScintilla as Scintilla, QsciLexerCustom as CustomLexer, QsciAPIs
from PyQt5.QtGui import QColor, QResizeEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar,\
    QTabWidget, QListWidget, QListWidgetItem, QWidget, QLineEdit, QPushButton
from getpass import getuser
from os import mkdir, path, walk

# variables
INITIAL_WINDOW_WIDTH = 1300
INITIAL_WINDOW_HEIGHT = 700
colors = {'main-bg': '#3c3f41',
          'default-bg': '#2b2b2b', 'default-text': '#a9b7c6',
          'keyword-text': '#cc7832', 'keyword-bg': '#2b2b2b',
          'decorator-text': '#bbb529', 'decorator-bg': '#2b2b2b',
          'builtin-text': '#8888c6', 'builtin-bg': '#2b2b2b',
          'comment-text': '#808080', 'comment-bg': '#2b2b2b',
          'string-text': '#6a8759', 'string-bg': '#2b2b2b',
          'int-text': '#6294ba', 'int-bg': '#2b2b2b',
          'self-text': '#94558d', 'self-bg': '#2b2b2b',
          'function-text': '#ffc66d', 'function-bg': '#2b2b2b',
          'special-text': '#b200b2', 'special-bg': '#2b2b2b'}

KEYWORDS = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
            'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
            'in', 'is', 'lambda', 'not', 'or', 'pass', 'return', 'try',
            'while', 'with', 'yield']

BUILTINS = ['print', 'len', 'range', 'int', 'str', 'bool', 'list', 'set', 'map']

# func_name_next = False
# string_color_mode = False
multiline_string_color_mode = False
# comment_color_mode = False
# decorator_color_mode = False
string_start_with = ''


# functions
# def new_project(dialog_parent):
#     text, ok = QInputDialog().getText(dialog_parent, "QInputDialog().getText()",
#                                       "Project name:", QLineEdit.Normal)

# Syntax Highlight class
class SyntaxHighlighter(CustomLexer):
    def __init__(self):
        super(SyntaxHighlighter, self).__init__()
        self.STYLES = {
            'default': 0,
            'keyword': 1,
            'decorator': 2,
            'builtin': 3,
            'comment': 4,
            'string': 5,
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
        global string_start_with, multiline_string_color_mode
        func_name_next = False
        string_color_mode = False
        comment_color_mode = False
        decorator_color_mode = False

        self.startStyling(start)

        text = self.parent().text()[start:end]

        # tokenizing text using regex
        tokenizer = compile(r'\{\.|\.\}|\#|\'|\"\"\"|\n|\s+|\w+|\W')
        tokens = [(token, len(token)) for token in tokenizer.findall(text)]

        # coloring tokens
        try:
            for i, token in enumerate(tokens):

                if '\r\n' in token[0]:
                    comment_color_mode = False
                    decorator_color_mode = False

                elif comment_color_mode:
                    self.setStyling(token[1], 4)
                elif string_color_mode or multiline_string_color_mode:
                    self.setStyling(token[1], 5)
                elif decorator_color_mode:
                    self.setStyling(token[1], 2)

                elif token[0] == '#' and not string_color_mode and not decorator_color_mode:
                    comment_color_mode = True
                    self.setStyling(token[1], 4)

                elif token[0] == '@' and not string_color_mode and not comment_color_mode:
                    decorator_color_mode = True
                    self.setStyling(token[1], 2)

                elif token[0] == "'":
                    self.setStyling(token[1], 5)
                    print(text, i)
                    if not string_color_mode or not multiline_string_color_mode:
                        string_color_mode = True
                        string_start_with = "'"
                        if tokens[i - 1][0] == tokens[-2][0] == "'":
                            multiline_string_color_mode = True

                    else:
                        if token[0] in string_start_with:
                            string_start_with = ''
                            string_color_mode = False
                            multiline_string_color_mode = False
                elif token[0] == '"':
                    self.setStyling(token[1], 5)
                    if not string_color_mode or not multiline_string_color_mode:
                        string_color_mode = True
                        string_start_with = '"'
                        if tokens[i - 1][0] == tokens[-2][0] == '"':
                            multiline_string_color_mode = True
                    else:
                        if token[0] in string_start_with:
                            string_start_with = ''
                            string_color_mode = False
                            multiline_string_color_mode = False

                elif token[0] in KEYWORDS:
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

                else:
                    self.setStyling(token[1], 0)
        except IndexError:
            pass


# main window class
class IDE(QMainWindow):
    def __init__(self):
        super(IDE, self).__init__()

        self.setGeometry(0, 0, INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT)
        self.setStyleSheet(f'background-color: {colors["main-bg"]}; border: flat;')

        self.editor = Scintilla(self)

        self.lexer = SyntaxHighlighter()

        self.editor.setLexer(self.lexer)
        self.lexer.setParent(self.editor)
        api = QsciAPIs(self.lexer)

        self.toolbar = QToolBar(self)

        self.show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.editor.resize(int(1100 / INITIAL_WINDOW_WIDTH * self.width()),
                           int(650 / INITIAL_WINDOW_HEIGHT * self.height()))
        self.editor.move(0, int(50 / INITIAL_WINDOW_HEIGHT * self.height()))


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        self.setGeometry(1900, 900, 1500, 900)
        self.setStyleSheet(f'background-color: {colors["main-bg"]}; border: flat;')

        if not path.exists(f'C:\\Users\\{getuser()}\\GlinaIDEProjects'):
            mkdir(f'C:\\Users\\{getuser()}\\GlinaIDEProjects')

        projects = list(walk(f'C:\\Users\\{getuser()}\\GlinaIDEProjects'))[0][1]

        self.tab_bar = QTabWidget(self)

        self.project_widget = QWidget()

        self.search_widget = QLineEdit(self.project_widget)
        self.search_widget.setStyleSheet(f'background: {colors["default-text"]}, color:{colors["default-text"]}')
        self.search_widget.setPlaceholderText('Поиск проектов')
        self.search_widget.resize(500, 100)
        self.search_widget.move(100, 0)

        self.add_project_widget = QPushButton(self.project_widget)
        self.add_project_widget.move(610, 0)
        self.add_project_widget.resize(300, 100)
        self.add_project_widget.setVisible(True)
        self.add_project_widget.setStyleSheet('border-image: url(static/add_project.png);')

        self.settings_widget = QWidget()

        self.settings_tab_bar = QTabWidget(self.settings_widget)

        self.theme_settings_widget = QWidget()

        self.settings_tab_bar.addTab(self.theme_settings_widget, 'Цвет')

        self.tab_bar.addTab(self.project_widget, "Проекты")
        self.tab_bar.addTab(self.settings_widget, 'Настройки')
        self.tab_bar.setTabPosition(QTabWidget.West)
        self.tab_bar.resize(1502, 902)
        self.tab_bar.setStyleSheet(f'Q')

        self.show()


# running the app
app = QApplication([])
welcome_window = WelcomeWindow()
exit(app.exec())
