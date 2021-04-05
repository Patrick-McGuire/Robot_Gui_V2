"""
Text box widget
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QFont

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class CompleteConsoleWidget(CustomBaseWidget):
    i = 0.0

    def __init__(self, tab, name, x, y, widgetInfo):
        self.clearButtonWidget = QPushButton()
        self.hideOKButtonWidget = QPushButton()
        self.titleBox = QLabel()
        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.STATUS_EVENT_TYPE)

        self.hideOK = False

        self.layout = QGridLayout()
        self.layout.addWidget(self.titleBox, 1, 1, 1, 2)
        self.layout.addWidget(self.clearButtonWidget, 2, 1)
        self.layout.addWidget(self.hideOKButtonWidget, 2, 2)
        self.QTWidget.setLayout(self.layout)

        self.textWidgetList = []

        self.source = "status_event"
        self.title = "Status Events"
        if widgetInfo is not None:
            if Constants.SOURCE_ATTRIBUTE in widgetInfo:
                self.source = widgetInfo[Constants.SOURCE_ATTRIBUTE]
            if Constants.TITLE_ATTRIBUTE in widgetInfo:
                self.title = widgetInfo[Constants.TITLE_ATTRIBUTE]

        self.clearButtonWidget.setText("clear")
        self.hideOKButtonWidget.setText("Hide OK")
        self.titleBox.setText(self.title)
        self.titleBox.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.clearButtonWidget.clicked.connect(self.ClearButtonPress)
        self.hideOKButtonWidget.clicked.connect(self.HideOK)

    def ClearButtonPress(self):
        self.returnEvents.append(["{}_clear".format(self.source), "press"])

    def HideOK(self):
        self.hideOK = not self.hideOK
        self.returnEvents.append(["{}_hide_ok".format(self.source), str(self.hideOK)])

        if self.hideOK:
            self.hideOKButtonWidget.setText("Show OK")
        else:
            self.hideOKButtonWidget.setText("Hide OK")

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            return

        data = dataPassDict[self.source]

        if type(data) != list:
            return

        if len(data) < len(self.textWidgetList):
            self.layout.removeWidget(self.textWidgetList[-1])
            self.textWidgetList[-1].deleteLater()
            del self.textWidgetList[-1]

        for i in range(len(data)):
            if len(data) > len(self.textWidgetList):
                self.textWidgetList.append(QLabel())
                self.textWidgetList[-1].setFont(QFont("Monospace", self.fontSize-1))
                self.layout.addWidget(self.textWidgetList[-1], len(self.textWidgetList) + 3, 1, 1, 2)

            self.textWidgetList[i].setText(data[i][0])
            self.textWidgetList[i].adjustSize()

            status = str(data[i][1])
            if status == "0":
                self.textWidgetList[i].setStyleSheet("color: green")
            elif status == "1":
                self.textWidgetList[i].setStyleSheet("color: yellow")
            elif status == "2":
                self.textWidgetList[i].setStyleSheet("color: red")
            else:
                self.textWidgetList[i].setStyleSheet("color: blue")

        self.QTWidget.adjustSize()

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor + "}")
        self.clearButtonWidget.setStyleSheet(colorString + " color: " + self.textColor)
        self.hideOKButtonWidget.setStyleSheet(colorString + " color: " + self.textColor)
        self.titleBox.setStyleSheet(colorString + " color: " + self.headerTextColor)

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.clearButtonWidget.setStyleSheet("color: black")
        self.hideOKButtonWidget.setStyleSheet("color: black")
        self.titleBox.setStyleSheet("color: black")

    def setFontInfo(self):
        self.QTWidget.setFont(QFont(self.font, self.fontSize))
        self.clearButtonWidget.setFont(QFont(self.font, self.fontSize))
        self.titleBox.setFont(QFont(self.font, self.fontSize))
        self.clearButtonWidget.adjustSize()
        self.QTWidget.adjustSize()
