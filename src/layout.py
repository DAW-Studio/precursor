from math import pi, cos, sin
from PySide6.QtWidgets import (
    QWidget,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout
)
from PySide6.QtCore import (
    Qt,
    QPointF,
    QPoint,
)


class StructuredLayout(QBoxLayout):
    def __init__(self, structure=None):
        self.layout_attributes = {
            "stretch": self.addStretch,
            "spacing": self.addSpacing
        }
        self._structure = []
        if structure:
            self.structure = structure

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        self.setStructure(value)

    def setStructure(self, structure):
        """Updates the layout based on the provided structure."""
        self.clear()
        self._structure = structure
        for item in structure:
            if isinstance(item, dict):
                for attr in self.layout_attributes:
                    value = item.get(attr)
                    if value != None: self.layout_attributes[attr](value)
            else:
                try:
                    super().addWidget(item)
                except:
                    try:
                        super().addLayout(item)
                    except:
                        self.addSpacerItem(item)
    
    def addWidget(self, *args):
        self.structure.append(args[0])
        return super().addWidget(*args)

    def addStretch(self, stretch: int = 0):
        """Adds a stretchable space to the layout."""
        super().addStretch(stretch)

    def addSpacing(self, spacing: int = 0):
        """Adds fixed space to the layout."""
        super().addSpacing(spacing)

    def clear(self):
        """Removes all widgets from the layout."""
        while self.count():
            item = self.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)


class VBoxLayout(QVBoxLayout, StructuredLayout):
    def __init__(self, structure=None, spacing=0, contents_margins=(0,0,0,0), alignment=None):
        QVBoxLayout.__init__(self)
        StructuredLayout.__init__(self, structure)
        self.setContentsMargins(*contents_margins)
        self.setSpacing(spacing)
        if alignment != None: self.setAlignment(alignment)


class HBoxLayout(QHBoxLayout, StructuredLayout):
    def __init__(self, structure=None, spacing=0, contents_margins=(0,0,0,0), alignment=None):
        QHBoxLayout.__init__(self)
        StructuredLayout.__init__(self, structure)
        self.setContentsMargins(*contents_margins)
        self.setSpacing(spacing)
        if alignment != None: self.setAlignment(alignment)


def orbit(widgets:list, point:QPointF|QPoint, radius:int):
    for i, widget in enumerate(widgets):
        angle = (i / len(widgets)) * 360
        radian = angle * (pi / 180)
        x = point.x() + radius * cos(radian)
        y = point.y() + radius * sin(radian)
        widget.move(int(x - widget.width() / 2), int(y - widget.height() / 2))