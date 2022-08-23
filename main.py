from PyQt5.QtWidgets import QApplication, QMainWindow
from sys import exit

# variables
INITIAL_WINDOW_WIDTH = 1300
INITIAL_WINDOW_HEIGHT = 700

# main window class


class IDE(QMainWindow):
    def __init__(self):
        super(IDE, self).__init__()

        self.setGeometry(0, 0, INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT)

        self.show()


# running the app
app = QApplication([])
window = IDE()
exit(app.exec())

