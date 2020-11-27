"""
Text box widget
"""

from PyQt5.QtWidgets import QLabel

from .CustomBaseWidget import CustomBaseWidget


class TextBoxWidget(CustomBaseWidget):
    def __init__(self, tab, x, y):
        super().__init__()

        self.QTWidget = QLabel(tab)
        self.QTWidget.move(x, y)
        self.UpdateText("HI")

    def UpdateText(self, text):
        self.QTWidget.setText(text)

    def Update(self, value):
        self.UpdateText(value)
