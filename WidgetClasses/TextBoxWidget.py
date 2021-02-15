"""
Text box widget
"""

import xml.etree.ElementTree as ElementTree

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class TextBoxWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.titleBox = QLabel()
        self.textBox = QLabel()
        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.CONFIGURABLE_TEXT_BOX_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.titleBox)
        layout.addWidget(self.textBox)
        self.QTWidget.setLayout(layout)

        self.xBuffer = 0
        self.yBuffer = 0
        self.maxWidth = 0

        self.boxFormat = widgetInfo[Constants.CONFIG_ATTRIBUTE]
        self.title = widgetInfo[Constants.TITLE_ATTRIBUTE]

        self.titleBox.setText(self.title)
        self.titleBox.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def customUpdate(self, dataPassDict):
        outString = ""

        longestLine = 0
        for line in self.boxFormat:
            longestLine = max(longestLine, len(line[0]))

        for line in self.boxFormat:
            spaces = " " * (longestLine - len(line[0]) + 2)  # Add two extra spaces to everything
            if line[1] in dataPassDict:
                newLine = "{0}{2}{1}".format(line[0], dataPassDict[line[1]], spaces)
            else:
                newLine = "{0}{2}{1}".format(line[0], "No Data", spaces)

            outString = outString + newLine + "\n"

        self.textBox.setText(outString[:-1])
        self.QTWidget.adjustSize()
        self.maxWidth = max(self.QTWidget.width(), self.maxWidth)  # Keep it from shrinking back down
        self.QTWidget.setMinimumWidth(self.maxWidth)

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: " + self.textColor + "}")
        self.textBox.setStyleSheet(colorString + " color: " + self.textColor)
        self.titleBox.setStyleSheet(colorString + " color: " + self.headerTextColor)

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.textBox.setStyleSheet("color: black")
        self.titleBox.setStyleSheet("color: black")

    def setFontInfo(self):
        self.QTWidget.setFont(QFont(self.font, self.fontSize))
        self.textBox.setFont(QFont("Monospace", self.fontSize))
        self.titleBox.setFont(QFont(self.font, self.fontSize))
        self.QTWidget.adjustSize()

    def customXMLStuff(self, tag):
        tag.set(Constants.TITLE_ATTRIBUTE, str(self.title))
        tag.set(Constants.TYPE_ATTRIBUTE, str(Constants.CONFIGURABLE_TEXT_BOX_TYPE))

        items = []
        for line in self.boxFormat:
            items.append(ElementTree.SubElement(tag, Constants.LINE_NAME))
            items[-1].set(Constants.LABEL_ATTRIBUTE, line[0])
            items[-1].set(Constants.VALUE_ATTRIBUTE, line[1])
