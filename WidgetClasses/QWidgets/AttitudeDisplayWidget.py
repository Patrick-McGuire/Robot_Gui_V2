import os
import cv2

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint

from WidgetClasses.WidgetHelpers import BasicImageDisplay


class AttitudeDisplayWidget(QLabel):
    def __init__(self, parentWidget: QWidget = None):
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
        self.crossHairImage = BasicImageDisplay.BasicImageDisplay(self, self.crossHair, self.size * 0.7)
        self.rollPointerImage = BasicImageDisplay.BasicImageDisplay(self, self.rollPointer, self.size * 0.05, y=10)
        self.rollIndicatorImage = BasicImageDisplay.BasicImageDisplay(self, self.rollIndicator, self.size * 0.9)

        self.refreshMask()

    def setSize(self, size):
        # TODO: Use the QWidget size functions instead of this sketchy one
        self.size = size

        self.setGeometry(0, 0, size, size)
        self.setMinimumWidth(size)
        self.setMinimumHeight(size)
        self.refreshMask()

        self.crossHairImage.setGeometry(size * 0.7)
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

        painter = QPainter(self)  # Blue background
        painter.setPen(QPen(QColor(30, 144, 255), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(30, 144, 255), Qt.SolidPattern))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.setPen(QPen(QColor(166, 99, 0), 0, Qt.SolidLine))  # Brown horizon
        painter.setBrush(QBrush(QColor(166, 99, 0), Qt.SolidPattern))

        centerX = int(self.width() / 2)
        centerY = int(self.height() / 2)
        pitchScaleFactor = (-1 / 50) * (self.height() / 2)

        painter.translate(centerX, centerY)  # Set our coordinate system to be centered on the widget
        painter.rotate(-self.roll)

        painter.drawRect(-r, pitchScaleFactor * self.pitch, 2 * r, r2)

        # Pitch marker
        lineWidth = int(self.width() / 200)
        fontSize = max(int(self.width() / 30), 8)
        shortLength = self.width() / 8
        longLength = self.width() / 4

        painter.setPen(QPen(Qt.white, lineWidth, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        spacing = 5  # Draw lines every 5 degrees
        nearestPitch = spacing * round(self.pitch / spacing)
        maxToDrawLine = int(abs((self.width() * 0.5) / (2 * pitchScaleFactor)))  # Figure out the biggest pitch to get a line drawn
        maxPitch = min(nearestPitch + maxToDrawLine + spacing, 180)
        minPitch = max(nearestPitch - maxToDrawLine, -180)

        for i in range(minPitch, maxPitch, spacing):
            nearestPitchDelta = (self.pitch - i) * pitchScaleFactor

            if i % 10 != 0:
                painter.drawLine(-shortLength / 2, nearestPitchDelta, shortLength / 2, nearestPitchDelta)
                textDistance = shortLength / 2
            else:
                painter.drawLine(-longLength / 2, nearestPitchDelta, longLength / 2, nearestPitchDelta)
                textDistance = longLength / 2

            painter.setFont(QFont("Helvetica", fontSize))
            painter.drawText(textDistance * 1.1, nearestPitchDelta + int(fontSize / 2), "{}".format(abs(i)))
            painter.drawText(-(textDistance * 1.1 + (fontSize - 2) * 2), nearestPitchDelta + int(fontSize / 2), "{:2}".format(abs(i)))

        self.rollIndicatorImage.setRotation(self.roll)  # Set roll image

    def setRollPitch(self, roll, pitch):
        if pitch > 180:
            pitch -= 360

        self.roll = roll
        self.pitch = pitch
