"""
Text box widget
"""

from PyQt5.QtWidgets import QLabel

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class TextBoxWidget(CustomBaseWidget):
    def __init__(self, tab, x, y, widgetInfo):
        widgetInfo[Constants.FONT_ATTRIBUTE] = "Monospace"  # Forcing a monospace font fixes some formatting
        super().__init__(QLabel(tab), x, y, configInfo=widgetInfo)
        self.xBuffer = 0
        self.yBuffer = 0

        self.boxFormat = widgetInfo[Constants.CONFIG_ATTRIBUTE]
        self.title = widgetInfo[Constants.TITLE_ATTRIBUTE]

    def customUpdate(self, dataPassDict):
        outString = self.title
        lines = 1
        maxLineLength = len(outString)

        for line in self.boxFormat:
            lines = lines + 1
            if line[1] in dataPassDict:
                newLine = "\n{0:20}{1}".format(line[0], dataPassDict[line[1]])
            else:
                newLine = "\n{0:20}{1}".format(line[0], "No Data")

            outString = outString + newLine
            if len(newLine) > maxLineLength:
                maxLineLength = len(newLine)

        self.QTWidget.setText(outString)
        self.QTWidget.adjustSize()
