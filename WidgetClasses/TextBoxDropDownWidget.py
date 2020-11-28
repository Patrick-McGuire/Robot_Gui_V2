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

    def update(self, dataPassDict):
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

        self.QTWidget.setMinimumWidth(maxLineLength * 7 + 10)
        self.QTWidget.setMaximumWidth(maxLineLength * 7 + 10)
        self.QTWidget.setMinimumHeight(lines * 20 + 50)
        self.QTWidget.setMaximumHeight(lines * 20 + 50)
        self.textBoxWidget.setText(outString)

        self.width = float(self.QTWidget.minimumWidth())
        self.height = float(self.QTWidget.minimumHeight())

    def setMenuItems(self, menuItemList):
        self.dropDownWidget.clear()
        self.dropDownWidget.addItems(menuItemList)

    def setColor(self, color):
        if color == "white":
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; background: rgb(255, 255, 255); color: black}")
            self.textBoxWidget.setStyleSheet("border: 1px solid black; background: rgb(255, 255, 255); color: black")
            self.dropDownWidget.setStyleSheet("color: black")
        elif color == "blue":
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; background: rgb(0, 0, 100); color: black}")
            self.textBoxWidget.setStyleSheet("border: 1px solid black; background: rgb(0, 0, 100); color: white")
            self.dropDownWidget.setStyleSheet("color: black")
        elif color == "default":
            self.QTWidget.setStyleSheet("color: black")
            self.textBoxWidget.setStyleSheet("color: black")
            self.dropDownWidget.setStyleSheet("color: black")
        else:
            self.QTWidget.setStyleSheet("color: black")
            self.textBoxWidget.setStyleSheet("color: black")
            self.dropDownWidget.setStyleSheet("color: black")
