"""
Specific widget to display ROV status
"""

import xml.etree.ElementTree as ElementTree

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants
from DataHelpers import getValueFromDictionary


class ROVStatusWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.statusBox = QLabel()
        self.armingBox = QLabel()
        self.modeBox = QLabel()

        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.ROV_STATUS_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.statusBox, 1, 1)
        layout.addWidget(self.armingBox, 2, 1)
        layout.addWidget(self.modeBox, 3, 1)
        self.QTWidget.setLayout(layout)

        if self.size is None:  # Set a default size
            self.size = 30
        self.title = None
        self.font = None
        self.fontSize = None

        self.statusSource = getValueFromDictionary(widgetInfo, "statusSource", "status")
        self.armedSource = getValueFromDictionary(widgetInfo, "armedSource", "armed")
        self.allowedToArmSource = getValueFromDictionary(widgetInfo, "allowedToArmSource", "allowedToArm")
        self.modeSource = getValueFromDictionary(widgetInfo, "modeSource", "driveMode")

        self.statusBox.setFont(QFont("Monospace", self.size))
        self.statusBox.setAlignment(QtCore.Qt.AlignCenter)
        self.statusBox.setMinimumWidth(self.size * 8)

        self.armingBox.setFont(QFont("Monospace", self.size))
        self.armingBox.setAlignment(QtCore.Qt.AlignCenter)
        self.armingBox.setMinimumWidth(self.size * 13)

        self.modeBox.setFont(QFont("Monospace", self.size))
        self.modeBox.setAlignment(QtCore.Qt.AlignCenter)

    def customUpdate(self, dataPassDict):
        faultStatus = 3
        canArm = True
        armed = True
        mode = "Unknown"

        if self.statusSource in dataPassDict:
            faultStatus = int(float(dataPassDict[self.statusSource]))
        if self.allowedToArmSource in dataPassDict:
            canArm = str(dataPassDict[self.allowedToArmSource]).lower() == "true"
        if self.armedSource in dataPassDict:
            armed = str(dataPassDict[self.armedSource]).lower() == "true"
        if self.modeSource in dataPassDict:
            mode = str(dataPassDict[self.modeSource])

        if faultStatus == 2:
            self.statusBox.setStyleSheet("color: red")
            self.statusBox.setText("Faulted")
        elif faultStatus == 1:
            self.statusBox.setStyleSheet("color: yellow")
            self.statusBox.setText("Warning")
        elif faultStatus == 0:
            self.statusBox.setStyleSheet("color: green")
            self.statusBox.setText("OK")
        else:
            self.statusBox.setStyleSheet("color: blue")
            self.statusBox.setText("Unknown")

        if not canArm:
            self.armingBox.setText("Arming Disabled")
            self.armingBox.setStyleSheet("color: red")
        else:
            self.armingBox.setStyleSheet("color: green")
            if armed:
                self.armingBox.setText("Armed")
            else:
                self.armingBox.setText("Ready to arm")

        self.modeBox.setText(mode)

        self.statusBox.adjustSize()
        self.armingBox.adjustSize()
        self.modeBox.adjustSize()
        self.QTWidget.adjustSize()

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor + "}")
        self.modeBox.setStyleSheet("color: " + self.textColor)

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.armingBox.setStyleSheet("color: black")
        self.statusBox.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set("statusSource", self.statusSource)
        tag.set("armedSource", self.armedSource)
        tag.set("allowedToArmSource", self.allowedToArmSource)
        tag.set("modeSource", self.modeSource)
