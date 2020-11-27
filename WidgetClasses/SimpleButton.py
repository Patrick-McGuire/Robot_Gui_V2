"""
Text box widget
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton

from .CustomBaseWidget import CustomBaseWidget


class SimpleButton(CustomBaseWidget):
    def __init__(self, tab, buttonText, xPos, yPos):
        QTWidget = QPushButton(tab, text=buttonText)
        QTWidget.setToolTip("Holy shit this works")
        QTWidget.clicked.connect(self.OnButtonPress)
        super().__init__(QTWidget, xPos, yPos)

    def OnButtonPress(self):
        print("HI")
