"""
Text box widget
"""

from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QComboBox
from PyQt5.QtGui import QFont

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class TextBoxDropDownWidget(CustomBaseWidget):
    i = 0.0

    def __init__(self, tab, name, x, y, widgetInfo):
        self.textBoxWidget = QLabel()
        self.dropDownWidget = QComboBox()

        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.DROP_DOWN_TEXT_BOX_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.dropDownWidget)
        layout.addWidget(self.textBoxWidget)
        self.QTWidget.setLayout(layout)

        self.xBuffer = 0
        self.yBuffer = 0

        self.source = "_"
        if widgetInfo is not None:
            if Constants.SOURCE_ATTRIBUTE in widgetInfo:
                self.source = widgetInfo[Constants.SOURCE_ATTRIBUTE]

        self.menuItems = []
        self.setMenuItems(["No data"])

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            self.textBoxWidget.setText("No Data")
            return
        dataStruct = dataPassDict[self.source]

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
            line[0] = line[0].replace("\t", "     ").rstrip()  # Do some formatting to convert tabs to spaces and ditch trailing spaces
            longestLine = max(longestLine, len(line[0]))

        for line in dataToPrint:
            spaces = " " * (longestLine - len(line[0]) + 2)  # Add two extra spaces to everything
            newLine = "{0}{2}{1}\n".format(line[0], str(line[1]).lstrip(), spaces)

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

    def setFontInfo(self):
        self.QTWidget.setFont(QFont(self.font, self.fontSize))
        self.dropDownWidget.setFont(QFont(self.font, self.fontSize))
        self.textBoxWidget.setFont(QFont("Monospace", self.fontSize))
        self.dropDownWidget.adjustSize()
        self.QTWidget.adjustSize()

    def customXMLStuff(self, tag):
        tag.set(Constants.SOURCE_ATTRIBUTE, str(self.source))
