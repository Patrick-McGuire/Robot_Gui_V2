"""
Specific widget to display Mission Controller status
"""

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants
from DataHelpers import getValueFromDictionary


class ROVStatusWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.statusBox = QLabel()
        self.missionNameBox = QLabel()

        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.MISSION_STATUS_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.statusBox, 1, 1)
        layout.addWidget(self.missionNameBox, 2, 1)
        self.QTWidget.setLayout(layout)

        if self.size is None:  # Set a default size
            self.size = 30
        self.title = None
        self.font = None
        self.fontSize = None

        self.statusSource = getValueFromDictionary(widgetInfo, "statusSource", "missionStatus")
        self.missionNameSource = getValueFromDictionary(widgetInfo, "missionNameSource", "missionName")

        self.statusBox.setFont(QFont("Monospace", self.size))
        self.statusBox.setAlignment(QtCore.Qt.AlignCenter)
        self.statusBox.setMinimumWidth(self.size * 8)

        self.missionNameBox.setFont(QFont("Monospace", self.size / 3))
        self.missionNameBox.setAlignment(QtCore.Qt.AlignCenter)
        self.missionNameBox.setMinimumWidth(self.size)

    def customUpdate(self, dataPassDict):
        status = str(getValueFromDictionary(dataPassDict, self.statusSource, "Unknown"))
        missionName = str(getValueFromDictionary(dataPassDict, self.missionNameSource, "Unknown"))

        self.statusBox.setText(status)
        self.missionNameBox.setText("Mission: {}".format(missionName))

        self.statusBox.adjustSize()
        self.missionNameBox.adjustSize()

        self.QTWidget.adjustSize()

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor + "}")
        self.missionNameBox.setStyleSheet("color: " + self.textColor)
        self.statusBox.setStyleSheet("color: " + self.textColor)

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.missionNameBox.setStyleSheet("color: black")
        self.statusBox.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set("statusSource", self.statusSource)
        tag.set("missionNameSource", self.missionNameSource)
