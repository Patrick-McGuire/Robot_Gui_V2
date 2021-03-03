import os
import math
import cv2

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint

from WidgetClasses.WidgetHelpers import BasicImageDisplay


class AttitudeDisplayWidget(QLabel):
    def __init__(self, parentWidget: QWidget):
        super().__init__(parentWidget)

        self.size = 200

        self.setGeometry(0, 0, 200, 200)

        self.roll = 0
        self.pitch = 0

        dirName = os.path.dirname(__file__)
        dirName = os.path.abspath(os.path.join(dirName, "../.."))
        self.crossHair = cv2.imread("{}/Assets/cross_hair.png".format(dirName), cv2.IMREAD_UNCHANGED)
        self.rollPointer = cv2.imread("{}/Assets/roll_pointer.png".format(dirName), cv2.IMREAD_UNCHANGED)
        self.rollIndicator = cv2.imread("{}/Assets/roll_dial_1.png".format(dirName), cv2.IMREAD_UNCHANGED)

        # Cross hair
        self.crossHairImage = BasicImageDisplay.BasicImageDisplay(self, self.crossHair, self.size * 0.5)
        self.rollPointerImage = BasicImageDisplay.BasicImageDisplay(self, self.rollPointer, self.size * 0.05, y=10)
        self.rollIndicatorImage = BasicImageDisplay.BasicImageDisplay(self, self.rollIndicator, self.size * 0.9)

        self.refreshMask()

    def setSize(self, size):
        self.size = size

        self.setGeometry(0, 0, size, size)
        self.refreshMask()

        print(size)

        self.crossHairImage.setGeometry(size * 0.5)
        self.rollPointerImage.setGeometry(size * 0.05, y=10)
        self.rollIndicatorImage.setGeometry(size * 0.9)

    def refreshMask(self):
        # Set up octagonal mask for painter
        cornerSize = self.width() / 8
        points = [
            QPoint(cornerSize, 0),
            QPoint(0, cornerSize),
            QPoint(0, self.height() - cornerSize),
            QPoint(cornerSize, self.height()),
            QPoint(self.width() - cornerSize, self.height()),
            QPoint(self.width(), self.height() - cornerSize),
            QPoint(self.height(), cornerSize),
            QPoint(self.height() - cornerSize, 0)
        ]
        poly = QPolygon(points)
        region = QRegion(poly)
        self.setMask(region)

    def paintEvent(self, e):
        # Horizon green rectangle
        r = self.size * 2  # Rectangle width
        r2 = self.size * 2  # Rectangle height

        painter = QPainter(self)
        painter.setPen(QPen(QColor(30, 144, 255), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(30, 144, 255), Qt.SolidPattern))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.setPen(QPen(QColor(0, 100, 0), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(0, 100, 0), Qt.SolidPattern))

        pitchScaleFactor = (-1 / 50) * (self.height() / 2)
        centerY = (self.height() / 2) + self.pitch * pitchScaleFactor * math.cos(math.radians(self.roll))
        centerX = (self.width() / 2) + self.pitch * pitchScaleFactor * math.sin(math.radians(self.roll))

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
        lineWidth = int(self.width() / 200)
        fontSize = max(int(self.width() / 30), 8)

        painter.setPen(QPen(Qt.white, lineWidth, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        shortLength = self.width() / 8
        longLength = self.width() / 4

        shortDeltaX = (shortLength / 2) * math.cos(math.radians(self.roll))
        shortDeltaY = (shortLength / 2) * math.sin(math.radians(self.roll))
        longDeltaX = (longLength / 2) * math.cos(math.radians(self.roll))
        longDeltaY = (longLength / 2) * math.sin(math.radians(self.roll))

        spacing = 5
        nearestPitch = spacing * round(self.pitch / spacing)
        maxToDrawLine = int(abs((self.width() * 0.5) / (2 * pitchScaleFactor)))  # Figure out the biggest pitch to get a line drawn
        maxPitch = min(nearestPitch + maxToDrawLine, 180)
        minPitch = max(nearestPitch - maxToDrawLine, -180)

        for i in range(minPitch, maxPitch, spacing):
            nearestPitchDelta = (self.pitch - i) * pitchScaleFactor
            lineCenterX = (self.width() / 2) + nearestPitchDelta * math.sin(math.radians(self.roll))
            lineCenterY = (self.height() / 2) + nearestPitchDelta * math.cos(math.radians(self.roll))

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

        # if self.roll != self.rollIndicatorImage.theta():
        self.rollIndicatorImage.setRotation(self.roll)  # Set roll image

    def setRollPitch(self, roll, pitch):
        self.roll = roll
        self.pitch = pitch
