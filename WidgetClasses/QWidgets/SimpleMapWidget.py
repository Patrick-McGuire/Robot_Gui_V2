import time

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint

from DataHelpers import interpolate, distanceBetweenPoints


class SimpleMapWidget(QLabel):
    def __init__(self, parentWidget: QWidget = None, pointsToKeep=200, pointSpacing=0.1):
        super().__init__(parentWidget)

        self.size = 200

        self.setGeometry(0, 0, 200, 200)

        self.padding = 20
        self.originSize = 20
        self.decimals = 2
        self.lastPointTime = time.time()
        self.newPointInterval = 1

        self.pointsToKeep = pointsToKeep
        self.distanceBetweenPoints = pointSpacing
        self.maxDistanceBetweenPoints = pointSpacing

        self.x_position = 0
        self.y_position = 0

        self.maxAxis = 0.1
        self.minAxis = -0.1

        self.oldPoints = []

    def setSize(self, size):
        # TODO: Use the QWidget size functions instead of this sketchy one
        self.size = size

        self.setGeometry(0, 0, size, size)
        self.setMinimumWidth(size)
        self.setMinimumHeight(size)

    def paintEvent(self, e):
        self.size = self.width()

        painter = QPainter(self)  # Blue background
        painter.setPen(QPen(QColor(30, 144, 255), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(30, 144, 255), Qt.SolidPattern))
        painter.drawRect(0, 0, self.width(), self.height())

        # Draw old points
        painter.setPen(QPen(QColor(10, 10, 10), 1, Qt.SolidLine))
        for i in range(1, len(self.oldPoints)):
            point = self.oldPoints[i]
            lastPoint = self.oldPoints[i - 1]

            [xPos, yPos] = self.pointToDrawLocation(point[0], point[1])
            [oldX, oldY] = self.pointToDrawLocation(lastPoint[0], lastPoint[1])
            painter.drawLine(int(xPos), int(yPos), oldX, oldY)

        # Draw current position
        [xPos, yPos] = self.pointToDrawLocation(self.x_position, self.y_position)

        if len(self.oldPoints) > 0:
            lastPoint = self.oldPoints[0]
            [oldX, oldY] = self.pointToDrawLocation(lastPoint[0], lastPoint[1])
            painter.drawLine(xPos, yPos, oldX, oldY)

        painter.setPen(QPen(QColor(255, 0, 0), 10, Qt.SolidLine))
        painter.drawPoint(int(xPos), int(yPos))

        # Draw origin axes
        painter.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))
        [originX, originY] = self.pointToDrawLocation(0, 0)
        painter.drawLine(originX, originY, originX + self.originSize, originY)
        painter.drawLine(originX, originY, originX, originY - self.originSize)

        # Draw X axis
        minXAxis = 0.1 * round(self.minAxis / 0.1) - 1
        maxXAxis = 0.1 * round(self.maxAxis / 0.1) + 1
        [minX, _] = self.pointToDrawLocation(minXAxis, 0)
        [maxX, _] = self.pointToDrawLocation(maxXAxis, 0)
        for x in range(minX, maxX, 50):
            painter.drawLine(x, self.height(), x, self.height() - 10)
            painter.drawLine(0, x, 10, x)

            [xPoint, _] = self.drawLocationToPoint(x, 0)
            if self.decimals == 0:
                xPoint = int(xPoint)
            else:
                xPoint = round(xPoint, self.decimals)

            xPointStr = str(xPoint)
            xOffset = 6 * len(xPointStr) / 2
            painter.drawText(x - xOffset, self.height() - 15, xPointStr)

    def pointToDrawLocation(self, x, y):
        out_x = interpolate(x, self.minAxis, self.maxAxis, self.padding + 10, self.width() - self.padding)
        out_y = interpolate(y, self.minAxis, self.maxAxis, self.height() - (self.padding + 10), self.padding)
        return [int(out_x), int(out_y)]

    def drawLocationToPoint(self, x, y):
        out_x = interpolate(x, self.padding + 10, self.width() - self.padding, self.minAxis, self.maxAxis)
        out_y = interpolate(y, self.height() - (self.padding + 10), self.padding, self.minAxis, self.maxAxis)
        return [out_x, out_y]

    def setXY(self, x, y):
        self.maxAxis = max(self.maxAxis, x, y)
        self.minAxis = min(self.minAxis, x, y)

        self.x_position = x
        self.y_position = y

        if x == 0:
            return
        if len(self.oldPoints) == 0:
            self.oldPoints = [[x, y]]
        else:
            if time.time() > self.lastPointTime + self.newPointInterval:
                self.oldPoints = ([[x, y]] + self.oldPoints)[:self.pointsToKeep]
                self.lastPointTime = time.time()

        realAxisSize = self.maxAxis - self.minAxis

        if realAxisSize < 1:
            self.decimals = 2
        elif 1 <= realAxisSize < 20:
            self.decimals = 1
        else:
            self.decimals = 0

        self.distanceBetweenPoints = min(realAxisSize / 20, self.maxDistanceBetweenPoints)
