import PyQt5.QtCore as QtCore

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.QWidgets import AttitudeDisplayWidget, CompassDisplayWidget, AltitudeSpeedIndicatorWidget


class FullFlightDisplay(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QWidget(tab)
        QTWidget.setObjectName(name)

        self.SpeedTextBox = QLabel()
        self.VSpeedTextBox = QLabel()
        self.AltitudeTextBox = QLabel()

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.FULL_FLIGHT_TYPE)

        self.HUDWidget = AttitudeDisplayWidget.AttitudeDisplayWidget()
        self.CompassWidget = CompassDisplayWidget.CompassDisplayWidget()
        self.AltitudeWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget()
        self.SpeedWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget(leftOriented=False, onScreenSpacingScale=1.5)
        self.VSpeedWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget(onScreenSpacingScale=2)

        layout = QGridLayout()
        layout.addWidget(self.SpeedWidget, 2, 1)
        layout.addWidget(self.HUDWidget, 2, 2)
        layout.addWidget(self.AltitudeWidget, 2, 3)
        layout.addWidget(self.VSpeedWidget, 2, 4)
        layout.addWidget(self.CompassWidget, 2, 5)

        layout.addWidget(self.SpeedTextBox, 1, 1)
        layout.addWidget(self.VSpeedTextBox, 1, 4)
        layout.addWidget(self.AltitudeTextBox, 1, 3)
        self.QTWidget.setLayout(layout)

        self.SpeedTextBox.setAlignment(QtCore.Qt.AlignCenter)
        self.AltitudeTextBox.setAlignment(QtCore.Qt.AlignCenter)
        self.VSpeedTextBox.setAlignment(QtCore.Qt.AlignCenter)

        self.SpeedTextBox.setText("GS")
        self.VSpeedTextBox.setText("VS")
        self.AltitudeTextBox.setText("Alt")

        self.pitchSource = "pitch"
        self.rollSource = "roll"
        self.yawSource = "yaw"
        self.altSource = "altitude"
        self.speedSource = "groundSpeed"
        self.vSpeedSource = "verticalSpeed"

        if self.size is None:  # Set a default size
            self.size = 200
        if self.transparent is None:
            self.transparent = False
        self.title = None

        if "rollSource" in widgetInfo:
            self.rollSource = widgetInfo["rollSource"]
        if "pitchSource" in widgetInfo:
            self.pitchSource = widgetInfo["pitchSource"]
        if "yawSource" in widgetInfo:
            self.yawSource = widgetInfo["yawSource"]
        if "altSource" in widgetInfo:
            self.altSource = widgetInfo["altSource"]
        if "speedSource" in widgetInfo:
            self.speedSource = widgetInfo["speedSource"]
        if "vSpeedSource" in widgetInfo:
            self.vSpeedSource = widgetInfo["vSpeedSource"]

        self.HUDWidget.setSize(self.size)
        self.CompassWidget.setSize(self.size)
        self.AltitudeWidget.setSize(self.size)
        self.SpeedWidget.setSize(self.size)
        self.VSpeedWidget.setSize(self.size)

        self.QTWidget.adjustSize()

    def customUpdate(self, dataPassDict):
        roll = 0
        pitch = 0
        yaw = 0
        altitude = 0
        groundSpeed = 0
        vSpeed = 0

        if self.rollSource in dataPassDict:
            roll = float(dataPassDict[self.rollSource])

        if self.pitchSource in dataPassDict:
            pitch = float(dataPassDict[self.pitchSource])

        if self.yawSource in dataPassDict:
            yaw = float(dataPassDict[self.yawSource])  # Convert to actual compass heading

        if self.altSource in dataPassDict:
            altitude = float(dataPassDict[self.altSource])

        if self.speedSource in dataPassDict:
            groundSpeed = float(dataPassDict[self.speedSource])

        if self.vSpeedSource in dataPassDict:
            vSpeed = float(dataPassDict[self.vSpeedSource])

        self.HUDWidget.setRollPitch(roll, pitch)
        self.CompassWidget.setYaw(yaw)
        self.AltitudeWidget.setValue(altitude)
        self.SpeedWidget.setValue(groundSpeed)
        self.VSpeedWidget.setValue(vSpeed)

        self.QTWidget.adjustSize()
        self.QTWidget.update()

    def setColorRGB(self, red, green, blue):
        self.SpeedTextBox.setStyleSheet("color: " + self.textColor)
        self.VSpeedTextBox.setStyleSheet("color: " + self.textColor)
        self.AltitudeTextBox.setStyleSheet("color: " + self.textColor)

        if self.transparent:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        else:
            colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + colorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set("pitchSource", self.pitchSource)
        tag.set("rollSource", self.rollSource)
        tag.set("yawSource", self.yawSource)
        tag.set("altSource", self.altSource)
        tag.set("speedSource", self.speedSource)
        tag.set("vSpeedSource", self.vSpeedSource)
