"""
Text box widget
"""

import xml.etree.ElementTree as ElementTree

from PyQt5.QtWidgets import QLabel

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class SimpleConsole(CustomBaseWidget):
    def __init__(self, tab, x, y, widgetInfo):
        widgetInfo[Constants.FONT_ATTRIBUTE] = "Monospace"  # Forcing a monospace font fixes some formatting
        super().__init__(QLabel(tab), x, y, configInfo=widgetInfo, widgetType=Constants.SIMPLE_CONSOLE_TYPE)
        self.xBuffer = 0
        self.yBuffer = 0

        self.title = "No Title"
        self.source = "testarray"

        if Constants.TITLE_ATTRIBUTE in widgetInfo:
            self.title = widgetInfo[Constants.TITLE_ATTRIBUTE]
        if Constants.SOURCE_ATTRIBUTE in widgetInfo:
            self.source = widgetInfo[Constants.SOURCE_ATTRIBUTE]

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            return

        outString = self.title
        data = dataPassDict[self.source]

        for line in reversed(data):
            outString = outString + "\n" + line

        self.QTWidget.setText(outString)
        self.QTWidget.adjustSize()

    def customXMLStuff(self, tag):
        tag.set(Constants.TITLE_ATTRIBUTE, str(self.title))
        tag.set(Constants.SOURCE_ATTRIBUTE, str(self.source))
