"""
Text box widget
"""

from PyQt5.QtWidgets import QLabel

from .CustomBaseWidget import CustomBaseWidget


class TextBoxWidget(CustomBaseWidget):
    def __init__(self, tab, x, y):
        super().__init__(QLabel(tab), x, y)

        self.boxFormat = [["line1", "test"], ["bbb", "test1"]]

        self.QTWidget.setStyleSheet("border: 1px solid black;")

    def Update(self, dataPassDict):
        outString = "Title:"
        lines = 1
        maxLineLength = len(outString)

        for line in self.boxFormat:
            lines = lines + 1
            if line[1] in dataPassDict:
                newLine = "\n{0}\t{1}".format(line[0], dataPassDict[line[1]])
            else:
                newLine = "\n{0}\t{1}".format(line[0], "No Data")

            outString = outString + newLine
            if len(newLine) > maxLineLength:
                maxLineLength = len(newLine)

        self.QTWidget.setMinimumWidth(maxLineLength*10)
        self.QTWidget.setMinimumHeight(lines*20)
        self.QTWidget.setText(outString)
