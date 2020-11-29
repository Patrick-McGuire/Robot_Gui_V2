"""
Text box widget
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class TextBoxWidget(CustomBaseWidget):
    def __init__(self, tab, x, y, widgetInfo):
        super().__init__(QLabel(tab), x, y)
        self.xBuffer = 0
        self.yBuffer = 0

        self.boxFormat = widgetInfo[Constants.CONFIG_ATTRIBUTE]
        font = widgetInfo[Constants.FONT_ATTRIBUTE]
        size = int(widgetInfo[Constants.FONT_SIZE_ATTRIBUTE])
        color = widgetInfo[Constants.BACKGROUND_ATTRIBUTE]

        self.QTWidget.setFont(QFont(font, size))

        self.setColor(color)

    def update(self, dataPassDict):
        outString = "Title:"
        lines = 1
        maxLineLength = len(outString)

        for line in self.boxFormat:
            lines = lines + 1
            if line[1] in dataPassDict:
                newLine = "\n{0:1}\t\t{1}".format(line[0], dataPassDict[line[1]])
            else:
                newLine = "\n{0:1}\t\t{1}".format(line[0], "No Data")

            outString = outString + newLine
            if len(newLine) > maxLineLength:
                maxLineLength = len(newLine)

        self.QTWidget.setText(outString)
        self.QTWidget.adjustSize()

        self.width = float(self.QTWidget.size().width())
        self.height = float(self.QTWidget.size().height())
