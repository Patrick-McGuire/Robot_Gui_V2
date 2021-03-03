import os
import math
import cv2

from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.WidgetHelpers import BasicImageDisplay


class AttitudeWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QLabel(tab)
        QTWidget.setObjectName(name)

        self.PainterWidget = QLabel(QTWidget)
        self.PainterWidget.setObjectName("{}_painter".format(name))

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.ATTITUDE_TYPE)

        self.roll = 0
        self.pitch = 0

        self.pitchSource = "pitch"
        self.rollSource = "roll"

        if self.size is None:  # Set a default size
            self.size = 200
        if self.transparent is None:
            self.transparent = True

        if "pitchSource" in widgetInfo:
            self.pitchSource = widgetInfo["pitchSource"]
        if "rollSource" in widgetInfo:
            self.rollSource = widgetInfo["rollSource"]

        self.setSize(self.size, self.size)
        self.PainterWidget.setGeometry(0, 0, self.size, self.size)

        dirName = os.path.dirname(__file__)
        dirName = os.path.abspath(os.path.join(dirName, ".."))
        self.crossHair = cv2.imread("{}/Assets/cross_hair.png".format(dirName), cv2.IMREAD_UNCHANGED)
        self.rollPointer = cv2.imread("{}/Assets/roll_pointer.png".format(dirName), cv2.IMREAD_UNCHANGED)
        self.rollIndicator = cv2.imread("{}/Assets/roll_dial_1.png".format(dirName), cv2.IMREAD_UNCHANGED)

        # Cross hair
        self.crossHairImage = BasicImageDisplay.BasicImageDisplay(self.QTWidget, self.crossHair, self.size * 0.5)
        self.rollPointerImage = BasicImageDisplay.BasicImageDisplay(self.QTWidget, self.rollPointer, self.size * 0.05, y=self.height / 40)
        self.rollIndicatorImage = BasicImageDisplay.BasicImageDisplay(self.QTWidget, self.rollIndicator, self.size * 0.95)

        self.PainterWidget.paintEvent = self.drawHUD  # Set up painter

        cornerSize = self.width / 8
        points = [
            QPoint(cornerSize, 0),
            QPoint(0, cornerSize),
            QPoint(0, self.height - cornerSize),
            QPoint(cornerSize, self.height),
            QPoint(self.width - cornerSize, self.height),
            QPoint(self.width, self.height - cornerSize),
            QPoint(self.height, cornerSize),
            QPoint(self.height - cornerSize, 0)
        ]
        poly = QPolygon(points)
        region = QRegion(poly)
        self.PainterWidget.setMask(region)

    def drawHUD(self, e):
        # Horizon green rectangle
        r = self.size * 2  # Rectangle width
        r2 = self.size * 2  # Rectangle height

        painter = QPainter(self.PainterWidget)
        painter.setPen(QPen(QColor(0, 100, 0), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(0, 100, 0), Qt.SolidPattern))

        pitchScaleFactor = (-1 / 50) * (self.height / 2)
        centerY = (self.height / 2) + self.pitch * pitchScaleFactor * math.cos(math.radians(self.roll))
        centerX = (self.width / 2) + self.pitch * pitchScaleFactor * math.sin(math.radians(self.roll))

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

        # Pitch marker
        lineWidth = int(self.width / 200)
        fontSize = max(int(self.width / 30), 8)

        painter.setPen(QPen(Qt.white, lineWidth, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        shortLength = self.width / 8
        longLength = self.width / 4

        shortDeltaX = (shortLength / 2) * math.cos(math.radians(self.roll))
        shortDeltaY = (shortLength / 2) * math.sin(math.radians(self.roll))
        longDeltaX = (longLength / 2) * math.cos(math.radians(self.roll))
        longDeltaY = (longLength / 2) * math.sin(math.radians(self.roll))

        spacing = 5
        nearestPitch = spacing * round(self.pitch / spacing)
        maxToDrawLine = int(abs((self.width * 0.5) / (2 * pitchScaleFactor)))  # Figure out the biggest pitch to get a line drawn
        maxPitch = min(nearestPitch + maxToDrawLine, 180)
        minPitch = max(nearestPitch - maxToDrawLine, -180)

        for i in range(minPitch, maxPitch, spacing):
            nearestPitchDelta = (self.pitch - i) * pitchScaleFactor
            lineCenterX = (self.width / 2) + nearestPitchDelta * math.sin(math.radians(self.roll))
            lineCenterY = (self.height / 2) + nearestPitchDelta * math.cos(math.radians(self.roll))

            if i % 10 != 0:
                startX = lineCenterX + shortDeltaX
                startY = lineCenterY - shortDeltaY
                endX = lineCenterX - shortDeltaX
                endY = lineCenterY + shortDeltaY
                textDistance = shortLength / 2
            else:
                startX = lineCenterX + longDeltaX
                startY = lineCenterY - longDeltaY
                endX = lineCenterX - longDeltaX
                endY = lineCenterY + longDeltaY
                textDistance = longLength / 2

            painter.drawLine(startX, startY, endX, endY)

            painter.translate(lineCenterX, lineCenterY)  # HOLY SHIT I DIDN'T KNOW YOU COULD DO THIS UNITL I GOT TO HERE
            painter.rotate(-self.roll)

            painter.setFont(QFont("Arial", fontSize))
            painter.drawText(textDistance * 1.1, int(fontSize / 2), "{}".format(abs(i)))
            painter.drawText(-(textDistance * 1.1 + (fontSize - 4) * 2), int(fontSize / 2), "{:2}".format(abs(i)))

            painter.rotate(self.roll)
            painter.translate(-lineCenterX, -lineCenterY)

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

        self.roll = roll
        self.pitch = pitch

        self.QTWidget.update()  # Call painter
        self.rollIndicatorImage.setRotation(roll)  # Set roll image

    def setColorRGB(self, red, green, blue):
        if self.transparent:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        else:
            colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + colorString + " color: " + self.textColor + "}")

        skyColorString = "background: rgb({0}, {1}, {2});".format(30, 144, 255)
        self.PainterWidget.setStyleSheet("QWidget#" + self.PainterWidget.objectName() + " {" + skyColorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set("pitchSource", self.pitchSource)
        tag.set("rollSource", self.rollSource)
