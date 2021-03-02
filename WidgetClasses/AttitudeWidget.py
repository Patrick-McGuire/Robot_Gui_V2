import os
import math
import cv2

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor
from PyQt5.QtCore import Qt, QPoint

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.WidgetHelpers import BasicImageDisplay


class AttitudeWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QLabel(tab)
        QTWidget.setObjectName(name)

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.ATTITUDE_TYPE)

        self.roll = 0
        self.pitch = 0

        if self.size is None:  # Set a default size
            self.size = 200

        self.setSize(self.size, self.size)

        dirName = os.path.dirname(__file__)
        dirName = os.path.abspath(os.path.join(dirName, ".."))
        self.crossHair = cv2.imread("{}/Assets/cross_hair.png".format(dirName), cv2.IMREAD_UNCHANGED)
        self.rollPointer = cv2.imread("{}/Assets/roll_pointer.png".format(dirName), cv2.IMREAD_UNCHANGED)
        self.rollIndicator = cv2.imread("{}/Assets/roll_dial_1.png".format(dirName), cv2.IMREAD_UNCHANGED)

        # Cross hair
        self.crossHairImage = BasicImageDisplay.BasicImageDisplay(self.QTWidget, self.crossHair, self.size * 0.5)
        self.rollPointerImage = BasicImageDisplay.BasicImageDisplay(self.QTWidget, self.rollPointer, self.size * 0.05, y=10)
        self.rollIndicatorImage = BasicImageDisplay.BasicImageDisplay(self.QTWidget, self.rollIndicator, self.size * 0.9)

        self.QTWidget.paintEvent = self.drawHUD  # Set up painter

    def drawHUD(self, e):
        r = 400  # Rectangle width
        r2 = 400  # Rectangle height

        painter = QPainter(self.QTWidget)
        painter.setPen(QPen(QColor(0, 100, 0), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(0, 100, 0), Qt.SolidPattern))

        centerY = ((self.pitch / 100) * (self.height / 2)) + (self.height / 2)
        centerX = self.width / 2

        xOffset = r * math.cos(math.radians(self.roll))
        yOffset = r * math.sin(math.radians(self.roll))

        xOffset2 = r2 * math.sin(math.radians(self.roll))
        yOffset2 = r2 * math.cos(math.radians(self.roll))

        points = [  # Ordered clockwise from (centerX, centerY)
            QPoint(centerX + xOffset, centerY - yOffset),
            QPoint(centerX + xOffset + xOffset2, centerY - yOffset + yOffset2),
            QPoint(centerX - xOffset + xOffset2, centerY + yOffset + yOffset2),
            QPoint(centerX - xOffset, centerY + yOffset)
        ]

        poly = QPolygon(points)
        painter.drawPolygon(poly)

    def customUpdate(self, dataPassDict):
        if "roll" not in dataPassDict:
            roll = 0
            pitch = 0
        else:
            roll = float(dataPassDict["roll"])
            pitch = float(dataPassDict["pitch"])

        if pitch > 180:
            pitch -= 360

        self.roll = roll
        self.pitch = pitch

        self.QTWidget.update()  # Call painter
        self.rollIndicatorImage.setRotation(roll)  # Set roll image

    def setColorRGB(self, red, green, blue):
        red = 30
        green = 144
        blue = 255

        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + colorString + " color: " + self.textColor + "}")

        # self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
