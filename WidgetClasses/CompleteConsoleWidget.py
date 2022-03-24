"""
Text box widget
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont, QKeyEvent

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class CompleteConsoleWidget(CustomBaseWidget):
    i = 0.0

    def __init__(self, tab, name, x, y, widgetInfo):
        self.textBoxWidget = QLabel()
        self.textEntryWidget = QLineEdit()
        self.titleBox = QLabel()
        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.COMPLETE_CONSOLE_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.titleBox)
        layout.addWidget(self.textEntryWidget)
        layout.addWidget(self.textBoxWidget)
        self.QTWidget.setLayout(layout)

        self.textEntryWidget.returnPressed.connect(self.returnPressed)

        self.oldKeyPress = self.textEntryWidget.keyPressEvent  # We want to use the old key press, but do our code first
        self.textEntryWidget.keyPressEvent = self.keyPressEvent

        self.xBuffer = 0
        self.yBuffer = 0

        self.source = "_"
        self.title = "No Title"
        if widgetInfo is not None:
            if Constants.SOURCE_ATTRIBUTE in widgetInfo:
                self.source = widgetInfo[Constants.SOURCE_ATTRIBUTE]
            if Constants.TITLE_ATTRIBUTE in widgetInfo:
                self.title = widgetInfo[Constants.TITLE_ATTRIBUTE]

        self.titleBox.setText(self.title)
        self.titleBox.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.commandHistory = []
        self.commandHistoryIndex = -1
        self.currentCommand = ""

    # ([value] + list)[:20]

    def keyPressEvent(self, eventQKeyEvent: QKeyEvent):
        if eventQKeyEvent.key() == 16777235:  # UP
            if self.commandHistoryIndex == -1:  # If we're editing the newest command
                self.currentCommand = self.textEntryWidget.text()
            if len(self.commandHistory) > 0:
                self.commandHistoryIndex = min(len(self.commandHistory) - 1, self.commandHistoryIndex + 1)
                self.textEntryWidget.setText(self.commandHistory[self.commandHistoryIndex])
        elif eventQKeyEvent.key() == 16777237:  # DOWN
            self.commandHistoryIndex = max(self.commandHistoryIndex - 1, -1)
            if self.commandHistoryIndex == -1:
                self.textEntryWidget.setText(self.currentCommand)
            else:
                self.textEntryWidget.setText(self.commandHistory[self.commandHistoryIndex])

        self.oldKeyPress(eventQKeyEvent)

    def returnPressed(self):
        text = self.textEntryWidget.text()
        self.textEntryWidget.clear()
        self.returnEvents.append([self.source, text])

        if len(self.commandHistory) == 0:
            self.commandHistory = [text]
        if self.commandHistory[0] != text:
            self.commandHistory = [text] + self.commandHistory

        self.currentCommand = ""
        self.commandHistoryIndex = -1

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            return

        outString = ""
        data = dataPassDict[self.source]

        for line in reversed(data[:10]):
            outString = outString + line + "\n"

        self.textBoxWidget.setText(outString[:-1])
        self.QTWidget.adjustSize()

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor + "}")
        self.textBoxWidget.setStyleSheet(colorString + " color: " + self.textColor)
        self.textEntryWidget.setStyleSheet("border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor)
        self.titleBox.setStyleSheet(colorString + " color: " + self.headerTextColor)

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.textBoxWidget.setStyleSheet("color: black")
        self.textEntryWidget.setStyleSheet("color: black")
        self.titleBox.setStyleSheet("color: black")

    def setFontInfo(self):
        self.QTWidget.setFont(QFont(self.font, self.fontSize))
        self.textEntryWidget.setFont(QFont(self.font, self.fontSize))
        self.textBoxWidget.setFont(QFont("Monospace", self.fontSize))
        self.titleBox.setFont(QFont(self.font, self.fontSize))
        self.textEntryWidget.adjustSize()
        self.QTWidget.adjustSize()
