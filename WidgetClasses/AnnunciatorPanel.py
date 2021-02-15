"""
Text box widget
"""

import PyQt5.QtCore as QtCore

from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class AnnunciatorPanel(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.titleWidget = QLabel()
        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.ANNUNCIATOR_TYPE)

        self.xBuffer = 0
        self.yBuffer = 0

        self.source = "_"
        self.title = ""
        if widgetInfo is not None:
            if Constants.SOURCE_ATTRIBUTE in widgetInfo:
                self.source = widgetInfo[Constants.SOURCE_ATTRIBUTE]
            if Constants.TITLE_ATTRIBUTE in widgetInfo:
                self.title = widgetInfo[Constants.TITLE_ATTRIBUTE]

        layout = QGridLayout()
        self.titleWidget.setText(self.title)
        self.titleWidget.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.titleWidget, 0, 0, 1, 3)

        self.annunciatorWidgets = []
        for column in range(2):
            for row in range(10):
                self.annunciatorWidgets.append(QLabel())
                self.annunciatorWidgets[-1].setMaximumWidth(150)
                self.annunciatorWidgets[-1].setMinimumWidth(150)
                layout.addWidget(self.annunciatorWidgets[-1], row+1, column)

        self.QTWidget.setLayout(layout)

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            return

        data = dataPassDict[self.source]

        for i in range(len(data)):
            self.annunciatorWidgets[i].setText(data[i][0])
            self.annunciatorWidgets[i].setToolTip(data[i][2])
            self.annunciatorWidgets[i].setToolTipDuration(5000)

            status = str(data[i][1])
            if status == "0":
                self.annunciatorWidgets[i].setStyleSheet("background: green; color: black")
            elif status == "1":
                self.annunciatorWidgets[i].setStyleSheet("background: yellow; color: black")
            elif status == "2":
                self.annunciatorWidgets[i].setStyleSheet("background: red; color: black")
            else:
                self.annunciatorWidgets[i].setStyleSheet("background: blue; color: black")

        for i in range(len(data), len(self.annunciatorWidgets)):  # Make the rest empty and green
            self.annunciatorWidgets[i].setText(" ")
            self.annunciatorWidgets[i].setStyleSheet("background: green; color: black")

        self.QTWidget.adjustSize()

    def setColorRGB(self, red: int, green: int, blue: int):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + "{" + "border: 1px solid " + self.borderColor + "; background: rgb({0}, {1}, {2}); color: {3}".format(red, green, blue, self.headerTextColor) + "}")
        self.titleWidget.setStyleSheet(colorString + " color: " + self.headerTextColor)

    def customXMLStuff(self, tag):
        tag.set(Constants.SOURCE_ATTRIBUTE, str(self.source))
        tag.set(Constants.TITLE_ATTRIBUTE, str(self.title))
