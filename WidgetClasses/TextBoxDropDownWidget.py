"""
Text box widget
"""

from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QComboBox

from .CustomBaseWidget import CustomBaseWidget


class TextBoxDropDownWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y):
        super().__init__(QWidget(tab), x, y)
        self.QTWidget.setObjectName(name)

        self.textBoxWidget = QLabel()
        self.dropDownWidget = QComboBox()

        layout = QGridLayout()
        layout.addWidget(self.dropDownWidget)
        layout.addWidget(self.textBoxWidget)
        self.QTWidget.setLayout(layout)

        self.xBuffer = 0
        self.yBuffer = 0

        self.boxFormat = [["line1", "test"], ["bbb", "test1"]]

        self.setMenuItems(["thing1", "thing2", "patrick"])

    def customUpdate(self, dataPassDict):
        outString = "Title:"
        lines = 1
        maxLineLength = len(outString)

        for line in self.boxFormat:
            lines = lines + 1
            if line[1] in dataPassDict:
                newLine = "\n{0:<15}{1}".format(line[0], dataPassDict[line[1]])
            else:
                newLine = "\n{0:<15}{1}".format(line[0], "No Data")

            outString = outString + newLine
            if len(newLine) > maxLineLength:
                maxLineLength = len(newLine)

        self.QTWidget.adjustSize()
        self.textBoxWidget.setText(outString)

        self.width = float(self.QTWidget.size().width())
        self.height = float(self.QTWidget.size().height())

    def setMenuItems(self, menuItemList):
        self.dropDownWidget.clear()
        self.dropDownWidget.addItems(menuItemList)

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        if max(red, green, blue) > 127:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: black}")
            self.textBoxWidget.setStyleSheet("border: 1px solid black; " + colorString + " color: black")
            self.dropDownWidget.setStyleSheet("color: black")
        else:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: white}")
            self.textBoxWidget.setStyleSheet("border: 1px solid black; " + colorString + " color: white")
            self.dropDownWidget.setStyleSheet("color: black")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.textBoxWidget.setStyleSheet("color: black")
        self.dropDownWidget.setStyleSheet("color: black")
