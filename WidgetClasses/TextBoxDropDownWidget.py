"""
Text box widget
"""

from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QComboBox
from PyQt5.QtGui import QFont

from .CustomBaseWidget import CustomBaseWidget


class TextBoxDropDownWidget(CustomBaseWidget):
    i = 0.0

    def __init__(self, tab, name, x, y):
        super().__init__(QWidget(tab), x, y)
        self.QTWidget.setObjectName(name)

        self.textBoxWidget = QLabel()
        self.dropDownWidget = QComboBox()
        self.textBoxWidget.setFont(QFont("Monospace", self.fontSize))

        layout = QGridLayout()
        layout.addWidget(self.dropDownWidget)
        layout.addWidget(self.textBoxWidget)
        self.QTWidget.setLayout(layout)

        self.xBuffer = 0
        self.yBuffer = 0

        self.boxFormat = [["line1", "test"], ["bbb", "test1"]]

        self.menuItems = []
        self.setMenuItems(["No data"])

    def customUpdate(self, dataPassDict):
        if "diagnostics_agg" not in dataPassDict:
            return
        dataStruct = dataPassDict["diagnostics_agg"]

        selectedTarget = self.dropDownWidget.currentText()
        menuItems = []
        for item in dataStruct:
            menuItems.append(item)
        self.setMenuItems(menuItems)

        if selectedTarget not in dataStruct:
            return
        dataToPrint = dataStruct[selectedTarget]

        outString = ""

        longestLine = 0
        for line in dataToPrint:
            longestLine = max(longestLine, len(line[0]))

        for line in dataToPrint:
            spaces = " " * (longestLine - len(line[0]) + 1)
            newLine = "{0}{2}\t{1}\n".format(line[0], line[1], spaces)

            outString = outString + newLine

        outString = outString[:-1]  # Remove last character

        self.textBoxWidget.setText(outString)
        self.QTWidget.adjustSize()

    def setMenuItems(self, menuItemList):
        if menuItemList != self.menuItems:
            self.dropDownWidget.clear()
            self.dropDownWidget.addItems(menuItemList)
        self.menuItems = menuItemList

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        if max(red, green, blue) > 127:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: black}")
            self.textBoxWidget.setStyleSheet("border: 1px solid black; " + colorString + " color: black")
            self.dropDownWidget.setStyleSheet(colorString + " color: black")
        else:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: white}")
            self.textBoxWidget.setStyleSheet("border: 1px solid black; " + colorString + " color: white")
            self.dropDownWidget.setStyleSheet(colorString + " color: white")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.textBoxWidget.setStyleSheet("color: black")
        self.dropDownWidget.setStyleSheet("color: black")
