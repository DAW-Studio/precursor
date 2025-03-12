import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSlider,
    QLabel
)
from PySide6.QtCore import Qt

class SliderWidget(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)

        self.setRange(0, 100)
        self.setValue(100)

        self.valueChanged.connect(self.update_label)
        