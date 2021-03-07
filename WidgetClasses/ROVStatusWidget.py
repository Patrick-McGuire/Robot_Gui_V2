"""
Specific widget to display ROV status
"""

import xml.etree.ElementTree as ElementTree

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class ROVStatusWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.statusBox = QLabel()
        self.armingBox = QLabel()

        super().__init__(QWidget(tab, objectName=name), x, y, configInfo=widgetInfo, widgetType=Constants.ROV_STATUS_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.statusBox, 1, 1)
        layout.addWidget(self.armingBox, 1, 2)
        self.QTWidget.setLayout(layout)

        if self.size is None:  # Set a default size
            self.size = 30

        self.statusSource = "status"
        self.armedSource = "armed"
        self.allowedToArmSource = "allowedToArm"

        if "statusSource" in widgetInfo:
            self.statusSource = widgetInfo["statusSource"]
        if "armedSource" in widgetInfo:
            self.armedSource = widgetInfo["armedSource"]
        if "allowedToArmSource" in widgetInfo:
            self.allowedToArmSource = widgetInfo["allowedToArmSource"]

        self.statusBox.setFont(QFont("Monospace", self.size))
        self.statusBox.setAlignment(QtCore.Qt.AlignCenter)
        self.statusBox.setMinimumWidth(self.size * 8)

        self.armingBox.setFont(QFont("Monospace", self.size))
        self.armingBox.setAlignment(QtCore.Qt.AlignCenter)
        self.armingBox.setMinimumWidth(self.size * 12)

    def customUpdate(self, dataPassDict):
        faultStatus = 3
        canArm = True
        armed = True

        if self.statusSource in dataPassDict:
            faultStatus = int(float(dataPassDict[self.statusSource]))
        if self.allowedToArmSource in dataPassDict:
            canArm = str(dataPassDict[self.allowedToArmSource]).lower() == "true"
        if self.armedSource in dataPassDict:
            armed = str(dataPassDict[self.armedSource]).lower() == "true"

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

        self.statusBox.adjustSize()
        self.armingBox.adjustSize()
        self.QTWidget.adjustSize()

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.armingBox.setStyleSheet("color: black")
        self.statusBox.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set("statusSource", self.statusSource)
        tag.set("armedSource", self.armedSource)
        tag.set("allowedToArmSource", self.allowedToArmSource)
