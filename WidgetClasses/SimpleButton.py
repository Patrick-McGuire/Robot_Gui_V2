"""
Text box widget
"""

from PyQt5.QtWidgets import QPushButton

from .CustomBaseWidget import CustomBaseWidget


class SimpleButton(CustomBaseWidget):
    def __init__(self, tab, buttonText, xPos, yPos):
        super().__init__()

        self.QTWidget = QPushButton(tab, text=buttonText)
        self.QTWidget.move(xPos, yPos)
