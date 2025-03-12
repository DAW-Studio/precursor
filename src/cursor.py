from PySide6.QtWidgets import (
    QWidget
)
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QCursor
)
from PySide6.QtCore import (
    Qt,
    QTimer
)

from pynput.mouse import Controller


class Cursor(QWidget):
    def __init__(self):
        super().__init__()
        print(QCursor().pixmap().size())
        self.mouse = Controller()
        self.image = QPixmap("resources/cursor.png").scaled(24,24,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setFixedSize(self.image.size())
        self.timer = QTimer()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, self.image)

    def show(self):
        self.move(*self.mouse.position)
        super().show()

    def moveEvent(self, event):
        return super().moveEvent(event)

    def move(self, x, y):
        super().move(x-self.width()/4, y-self.height()/4)
