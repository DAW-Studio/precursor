import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QSlider,
    QLabel,
    QPushButton,
    QLineEdit
)
from PySide6.QtGui import (
    QCursor,
    QPainter,
    QPen,
    QColor
)
from PySide6.QtCore import (
    Qt,
    QEvent,
    QTimer,
)

from layout import HBoxLayout, VBoxLayout

from cursor import Cursor

from shortcuts import Shortcuts
from tracker import Tracker
import time

from hotreload import HotReload


class Slider(QSlider):
    def __init__(self, tracker):
        super().__init__(Qt.Horizontal)
        self.tracker = tracker

    def paintEvent(self, event):
        super().paintEvent(event)  # Draw the default slider appearance

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the pen for drawing lines
        pen = QPen(QColor(255, 0, 0))  # Red lines
        pen.setWidth(2)
        painter.setPen(pen)

        # Draw lines at snap points
        for point in self.tracker.pauses:
            # Calculate the position of the snap point on the slider
            position = self.valueToPosition(point) 
            painter.drawLine(position, 0, position, self.height())

    def valueToPosition(self, value):
        # Converts the slider value to a position on the slider's axis
        return int(self.width() * (value - self.minimum()+2) / (self.maximum()-2 - self.minimum()+2))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300,80)
        self.setContentsMargins(20,0,20,0)

        self.cursor = Cursor()

        self.tracker = Tracker()
        self.tracker.start()

        self.timer = QTimer()

        self.main_widget = QLabel()
        self.main_widget.setContentsMargins(20,0,20,0)
        self.main_widget.setObjectName("main-widget")

        self.time_entry = QLineEdit(str(self.tracker.duration))
        self.time_entry.textEdited.connect(self.editDuration)
        self.time_entry.setFixedWidth(26)
        self.time_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider = Slider(self.tracker)
        self.slider.valueChanged.connect(self.moveCursor)

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.clicked.connect(self.moveMouse)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.hide)
    
        self.main_widget.setLayout(VBoxLayout([
            HBoxLayout([
                self.time_entry,
                self.slider
            ], spacing=5),
            HBoxLayout([
                self.ok_btn,
                self.cancel_btn
            ], spacing=10)
        ], spacing=5, alignment=Qt.AlignmentFlag.AlignVCenter))
        self.setCentralWidget(self.main_widget)
        self.setFocus()
    

    def editDuration(self, edit):
        self.tracker.duration = int(edit)
        self.time_entry.setText(edit)

    def moveCursor(self, value):
        print(self.tracker.pauses)
        closest_point = min(self.tracker.pauses, key=lambda x: abs(x - value))
        if abs(value - closest_point) <= 5:
            self.slider.setValue(closest_point)
            value = self.slider.value()
        x, y, t = self.tracker.timeline[value]
        self.cursor.move(x, y)

    def moveMouse(self):
        x, y, t = self.tracker.timeline[self.slider.value()]
        self.cursor.mouse.position = (x, y)
        self.hide()

    def event(self, event):
        if event.type() == QEvent.WindowDeactivate:
            self.hide()
        if event.type() == QEvent.KeyRelease:
            key = event.key()
            if key == 16777220:
                self.moveMouse()
            elif key == 16777216:
                self.hide()
        return super().event(event)

    def open(self):
        self.timer.singleShot(100, self.cursor.show)

        self.tracker.tracking = False

        self.slider.setRange(0,len(self.tracker.timeline)-1)
        self.slider.setValue(len(self.tracker.timeline)-1)

        self.timer.singleShot(200, self.show)

    def show(self):
        cpos = self.cursor.pos()
        self.move(cpos.x()-self.width()/2,cpos.y()+self.height()/2+20)
        super().show()
        self.raise_()
    
    def hide(self):
        self.cursor.hide()
        self.tracker.tracking = True
        self.tracker.timeline = []
        super().hide()
        


if __name__ == "__main__":
    app = QApplication()

    with open("resources/style.css", "r") as f:
        app.setStyleSheet(f.read())

    window = Window()
    window.show()
    window.hide()
    Shortcuts({"<alt>+<ctrl>+q": window.open}).start()
    HotReload(hotkey="<cmd>+s").start()

    sys.exit(app.exec()) 