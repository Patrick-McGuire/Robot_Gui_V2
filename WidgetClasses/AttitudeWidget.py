import os
import math
import cv2

from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.WidgetHelpers import BasicImageDisplay
from WidgetClasses.QWidgets import AttitudeDisplayWidget


class AttitudeWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QLabel(tab)
        QTWidget.setObjectName(name)

        self.HUDWidget = AttitudeDisplayWidget.AttitudeDisplayWidget(QTWidget)
        # self.HUDWidget.setGeometry(0, 0, 200, 200)

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.ATTITUDE_TYPE)

        self.pitchSource = "pitch"
        self.rollSource = "roll"

        if self.size is None:  # Set a default size
            self.size = 200
        if self.transparent is None:
            self.transparent = True
        self.title = None

        if "pitchSource" in widgetInfo:
            self.pitchSource = widgetInfo["pitchSource"]
        if "rollSource" in widgetInfo:
            self.rollSource = widgetInfo["rollSource"]

        self.setSize(self.size, self.size)
        self.HUDWidget.setSize(self.size)

    def customUpdate(self, dataPassDict):
        if self.rollSource not in dataPassDict:
            roll = 0
        else:
            roll = float(dataPassDict[self.rollSource])

        if self.pitchSource not in dataPassDict:
            pitch = 0
        else:
            pitch = float(dataPassDict[self.pitchSource])

        if pitch > 180:
            pitch -= 360

        self.HUDWidget.setRollPitch(roll, pitch)
        self.HUDWidget.update()

    def setColorRGB(self, red, green, blue):
        if self.transparent:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        else:
            colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + colorString + " color: " + self.textColor + "}")

        skyColorString = "background: rgb({0}, {1}, {2});".format(30, 144, 255)
        # self.PainterWidget.setStyleSheet("QWidget#" + self.PainterWidget.objectName() + " {" + skyColorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set("pitchSource", self.pitchSource)
        tag.set("rollSource", self.rollSource)
