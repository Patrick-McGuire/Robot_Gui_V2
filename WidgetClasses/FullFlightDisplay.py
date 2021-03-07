import xml.etree.ElementTree as ElementTree
import PyQt5.QtCore as QtCore

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.QWidgets import AttitudeDisplayWidget, CompassDisplayWidget, AltitudeSpeedIndicatorWidget, VSpeedIndicatorWidget


def getXMLAttribute(XLM, attribute: str, default: str):
    if XLM.hasAttribute(attribute):
        return XLM.getAttribute(attribute)
    else:
        return default


class FullFlightDisplay(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QWidget(tab)
        QTWidget.setObjectName(name)

        self.SpeedTextBox = QLabel()
        self.VSpeedTextBox = QLabel()
        self.AltitudeTextBox = QLabel()
        self.TerrainTextBox = QLabel()

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.FULL_FLIGHT_TYPE)

        if self.size is None:  # Set a default size
            self.size = 200
        if self.transparent is None:
            self.transparent = False
        self.title = None

        self.pitchSource = "pitch"
        self.rollSource = "roll"
        self.yawSource = "yaw"
        self.altSource = "altitude"
        self.speedSource = "groundSpeed"
        self.vSpeedSource = "verticalSpeed"
        self.terrainAltSource = "terrainAlt"

        self.useAltVSpeedWidget = False
        self.compassBelow = False
        self.useTerrainAltWidget = False
        self.altScale = 1
        self.vSpeedScale = 1
        self.terrainAltScale = 1

        if Constants.CONFIG_ATTRIBUTE in widgetInfo:  # Better way to get data
            configInfo = widgetInfo[Constants.CONFIG_ATTRIBUTE]

            if len(configInfo[0]) > 0:
                compass = configInfo[0][0]
                self.compassBelow = compass.getAttribute("compassBelow").lower() == "true"
                self.yawSource = compass.getAttribute("yawSource")

                attitude = configInfo[1][0]
                self.rollSource = attitude.getAttribute("rollSource")
                self.pitchSource = attitude.getAttribute("pitchSource")

                vSpeed = configInfo[2][0]
                self.vSpeedSource = vSpeed.getAttribute(Constants.SOURCE_ATTRIBUTE)
                self.useAltVSpeedWidget = vSpeed.getAttribute("useAltVSpeedWidget").lower() == "true"
                self.vSpeedScale = float(vSpeed.getAttribute(Constants.SCALE_ATTRIBUTE))

                terrainAlt = configInfo[3][0]
                self.useTerrainAltWidget = terrainAlt.getAttribute(Constants.ENABLED_ATTRIBUTE).lower() == "true"
                self.terrainAltSource = terrainAlt.getAttribute(Constants.SOURCE_ATTRIBUTE)
                self.terrainAltScale = float(terrainAlt.getAttribute(Constants.SCALE_ATTRIBUTE))

                altitude = configInfo[4][0]
                self.altSource = altitude.getAttribute(Constants.SOURCE_ATTRIBUTE)
                self.altScale = float(getXMLAttribute(altitude, Constants.SCALE_ATTRIBUTE, "1"))

                groundSpeed = configInfo[5][0]
                self.speedSource = groundSpeed.getAttribute(Constants.SOURCE_ATTRIBUTE)

        self.HUDWidget = AttitudeDisplayWidget.AttitudeDisplayWidget()
        self.CompassWidget = CompassDisplayWidget.CompassDisplayWidget()
        self.AltitudeWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget(onScreenSpacingScale=5)
        self.SpeedWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget(leftOriented=False, onScreenSpacingScale=1.5)
        self.TerrainAltWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget(onScreenSpacingScale=self.terrainAltScale)

        if self.useAltVSpeedWidget:
            self.VSpeedWidget = VSpeedIndicatorWidget.VSpeedIndicatorWidget(maxSpeed=self.vSpeedScale)
        else:
            self.VSpeedWidget = AltitudeSpeedIndicatorWidget.AltitudeSpeedIndicatorWidget(onScreenSpacingScale=self.vSpeedScale)

        layout = QGridLayout()
        layout.addWidget(self.SpeedWidget, 2, 1)
        layout.addWidget(self.HUDWidget, 2, 2)
        layout.addWidget(self.AltitudeWidget, 2, 3)
        layout.addWidget(self.VSpeedWidget, 2, 4)

        if self.compassBelow:
            layout.addWidget(self.CompassWidget, 3, 2)
        else:
            layout.addWidget(self.CompassWidget, 2, 5)

        if self.useTerrainAltWidget:
            layout.addWidget(self.TerrainAltWidget, 2, 0)
            layout.addWidget(self.TerrainTextBox, 1, 0)

        layout.addWidget(self.SpeedTextBox, 1, 1)
        layout.addWidget(self.VSpeedTextBox, 1, 4)
        layout.addWidget(self.AltitudeTextBox, 1, 3)
        self.QTWidget.setLayout(layout)

        self.SpeedTextBox.setAlignment(QtCore.Qt.AlignCenter)
        self.AltitudeTextBox.setAlignment(QtCore.Qt.AlignCenter)
        self.VSpeedTextBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TerrainTextBox.setAlignment(QtCore.Qt.AlignCenter)

        self.SpeedTextBox.setText("GS")
        self.VSpeedTextBox.setText("VS")
        self.AltitudeTextBox.setText("ALT")
        self.TerrainTextBox.setText("TER")

        self.HUDWidget.setSize(self.size)
        self.CompassWidget.setSize(self.size)
        self.AltitudeWidget.setSize(self.size)
        self.SpeedWidget.setSize(self.size)
        self.VSpeedWidget.setSize(self.size)
        self.TerrainAltWidget.setSize(self.size)

        self.QTWidget.adjustSize()

    def customUpdate(self, dataPassDict):
        roll = 0
        pitch = 0
        yaw = 0
        altitude = 0
        groundSpeed = 0
        vSpeed = 0
        terrainAlt = 0

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

        if self.terrainAltSource in dataPassDict:
            terrainAlt = float(dataPassDict[self.terrainAltSource])

        self.HUDWidget.setRollPitch(roll, pitch)
        self.CompassWidget.setYaw(yaw)
        self.AltitudeWidget.setValue(altitude)
        self.SpeedWidget.setValue(groundSpeed)
        self.VSpeedWidget.setValue(vSpeed)
        self.TerrainAltWidget.setValue(terrainAlt)

        self.QTWidget.adjustSize()
        self.QTWidget.update()

    def setColorRGB(self, red, green, blue):
        self.SpeedTextBox.setStyleSheet("color: " + self.textColor)
        self.VSpeedTextBox.setStyleSheet("color: " + self.textColor)
        self.AltitudeTextBox.setStyleSheet("color: " + self.textColor)
        self.TerrainTextBox.setStyleSheet("color:" + self.textColor)

        if self.transparent:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        else:
            colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        items = [ElementTree.SubElement(tag, "attitude")]
        items[-1].set("rollSource", self.rollSource)
        items[-1].set("pitchSource", self.pitchSource)

        items = [ElementTree.SubElement(tag, "compass")]
        items[-1].set("yawSource", self.yawSource)
        items[-1].set("compassBelow", str(self.compassBelow))

        items = [ElementTree.SubElement(tag, "vSpeed")]
        items[-1].set(Constants.SOURCE_ATTRIBUTE, self.vSpeedSource)
        items[-1].set("useAltVSpeedWidget", str(self.useAltVSpeedWidget))
        items[-1].set(Constants.SCALE_ATTRIBUTE, str(self.vSpeedScale))

        items = [ElementTree.SubElement(tag, "terrainAlt")]
        items[-1].set(Constants.ENABLED_ATTRIBUTE, str(self.useTerrainAltWidget))
        items[-1].set(Constants.SOURCE_ATTRIBUTE, self.terrainAltSource)
        items[-1].set(Constants.SCALE_ATTRIBUTE, str(self.terrainAltScale))

        items = [ElementTree.SubElement(tag, "altitude")]
        items[-1].set(Constants.SOURCE_ATTRIBUTE, self.altSource)
        items[-1].set(Constants.SCALE_ATTRIBUTE, str(int(self.altScale)))

        items = [ElementTree.SubElement(tag, "groundSpeed")]
        items[-1].set(Constants.SOURCE_ATTRIBUTE, self.speedSource)
