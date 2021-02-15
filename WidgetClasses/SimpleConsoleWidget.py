"""
Text box widget
"""
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class SimpleConsole(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.titleBox = QLabel()
        self.textBox = QLabel()
        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.SIMPLE_CONSOLE_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.titleBox)
        layout.addWidget(self.textBox)
        self.QTWidget.setLayout(layout)

        self.xBuffer = 0
        self.yBuffer = 0

        self.title = "No Title"
        self.source = "testarray"

        if Constants.TITLE_ATTRIBUTE in widgetInfo:
            self.title = widgetInfo[Constants.TITLE_ATTRIBUTE]
        if Constants.SOURCE_ATTRIBUTE in widgetInfo:
            self.source = widgetInfo[Constants.SOURCE_ATTRIBUTE]

        self.titleBox.setText(self.title)
        self.titleBox.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            return

        outString = ""
        data = dataPassDict[self.source]

        for line in reversed(data):
            outString += line + "\n"

        self.textBox.setText(outString[:-1])
        self.textBox.adjustSize()
        self.QTWidget.adjustSize()

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: " + self.textColor + "}")
        self.textBox.setStyleSheet(colorString + " color: " + self.textColor)
        self.titleBox.setStyleSheet(colorString + " color: " + self.textColor)

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.textBox.setStyleSheet("color: black")
        self.titleBox.setStyleSheet("color: black")

    def setFontInfo(self):
        self.QTWidget.setFont(QFont(self.font, self.fontSize))
        self.textBox.setFont(QFont("Monospace", self.fontSize))
        self.titleBox.setFont(QFont(self.font, self.fontSize))
        self.QTWidget.adjustSize()
