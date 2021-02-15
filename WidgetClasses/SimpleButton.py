"""
Text box widget
"""

from PyQt5.QtWidgets import QPushButton

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class SimpleButton(CustomBaseWidget):
    def __init__(self, tab, xPos, yPos, widgetInfo):
        QTWidget = QPushButton(tab)
        QTWidget.clicked.connect(self.OnButtonPress)
        super().__init__(QTWidget, xPos, yPos, configInfo=widgetInfo, widgetType=Constants.SIMPLE_BUTTON_TYPE)

        self.QTWidget.setText(self.title)
        self.QTWidget.adjustSize()

        self.source = "button"
        if Constants.SOURCE_ATTRIBUTE in widgetInfo:
            self.source = widgetInfo[Constants.SOURCE_ATTRIBUTE]

    def OnButtonPress(self):
        self.returnEvents.append([self.source, "press"])

    def setColorRGB(self, red: int, green: int, blue: int):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet(colorString + " color: " + self.textColor)


    def customXMLStuff(self, tag):
        tag.set(Constants.SOURCE_ATTRIBUTE, str(self.source))
