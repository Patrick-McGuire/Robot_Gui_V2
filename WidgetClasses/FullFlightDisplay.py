from PyQt5.QtWidgets import QWidget, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.QWidgets import AttitudeDisplayWidget, CompassDisplayWidget, AltitudeSpeedIndicatorWidget


class FullFlightDisplay(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QWidget(tab)
        QTWidget.setObjectName(name)

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.ATTITUDE_TYPE)

        self.HUDWidget = AttitudeDisplayWidget.AttitudeDisplayWidget()
        self.CompassWidget = CompassDisplayWidget.CompassDisplayWidget()
        self.AltitudeWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget()
        self.SpeedWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget(leftOriented=False)

        layout = QGridLayout()
        layout.addWidget(self.HUDWidget, 1, 2)
        # layout.addWidget(self.CompassWidget, 1, 2)
        layout.addWidget(self.AltitudeWidget, 1, 3)
        layout.addWidget(self.SpeedWidget, 1, 1)
        self.QTWidget.setLayout(layout)

        self.pitchSource = "pitch"
        self.rollSource = "roll"
        self.yawSource = "yaw"
        self.altSource = "altitude"
        self.speedSource = "groundSpeed"

        if self.size is None:  # Set a default size
            self.size = 200
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
            self.speedSource = widgetInfo["SpeedSource"]

        self.HUDWidget.setSize(self.size)
        self.CompassWidget.setSize(self.size)
        self.AltitudeWidget.setSize(self.size)
        self.SpeedWidget.setSize(self.size)

        self.QTWidget.adjustSize()

    def customUpdate(self, dataPassDict):
        roll = 0
        pitch = 0
        yaw = 0
        altitude = 0
        groundSpeed = 0

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

        self.HUDWidget.setRollPitch(roll, pitch)
        self.CompassWidget.setYaw(yaw)
        self.AltitudeWidget.setValue(altitude)
        self.SpeedWidget.setValue(groundSpeed)

        self.QTWidget.adjustSize()
        self.QTWidget.update()

    def setColorRGB(self, red, green, blue):
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
