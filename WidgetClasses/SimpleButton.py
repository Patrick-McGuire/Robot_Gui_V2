"""
Text box widget
"""

from PyQt5.QtWidgets import QPushButton

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class SimpleButton(CustomBaseWidget):
    def __init__(self, tab, buttonText, xPos, yPos):
        QTWidget = QPushButton(tab, text=buttonText)
        QTWidget.clicked.connect(self.OnButtonPress)
        super().__init__(QTWidget, xPos, yPos, widgetType=Constants.SIMPLE_BUTTON_TYPE)

    def OnButtonPress(self):
        print("HI")

    def setColorRGB(self, red: int, green: int, blue: int):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        if max(red, green, blue) > 127:
            self.QTWidget.setStyleSheet(colorString + " color: black")
        else:
            self.QTWidget.setStyleSheet(colorString + " color: white")
