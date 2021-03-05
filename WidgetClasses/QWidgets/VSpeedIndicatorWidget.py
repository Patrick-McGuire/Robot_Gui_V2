from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint


def clamp(value, minValue, maxValue):
    """
    Clamps a value between the min and max value
    """
    return min(max(value, minValue), maxValue)


def interpolate(value, in_min, in_max, out_min, out_max):
    """
    Interpolates a value from the input range to the output range
    """
    in_span = in_max - in_min
    out_span = out_max - out_min

    scaled = float(value - in_min) / float(in_span)
    return out_min + (scaled * out_span)


class VSpeedIndicatorWidget(QLabel):
    def __init__(self, parentWidget: QWidget = None, leftOriented=True, onScreenSpacingScale=1):
        super().__init__(parentWidget)

        self.size = 200

        self.spacing = 1  # Delta Value between lines
        self.onScreenSpacingScale = onScreenSpacingScale * 10  # Delta Pixels between lines
        self.value = 0

        self.leftOriented = leftOriented

    def setSize(self, size):
        # TODO: Use the QWidget size functions instead of this sketchy one
        self.size = size

        width = size / 6

        self.setGeometry(0, 0, width, size)
        self.setMinimumWidth(width)
        self.setMinimumHeight(size)

    def paintEvent(self, e):
        painter = QPainter(self)  # Grey background
        painter.setPen(QPen(QColor(50, 50, 50), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(50, 50, 50), Qt.SolidPattern))

        cornerX = self.width() / 2
        cornerY = self.height() / 8
        cornerHeight = self.height() / 4

        points = [
            QPoint(0, cornerY),
            QPoint(cornerX, cornerY),
            QPoint(self.width(), cornerHeight),
            QPoint(self.width(), self.height() - cornerHeight),
            QPoint(cornerX, self.height() - cornerY),
            QPoint(0, self.height() - cornerY)
        ]
        poly = QPolygon(points)
        painter.drawPolygon(poly)

        maxSpeed = 6
        speedIncrement = 1
        numberIncrement = 2
        gaugeHeight = self.height() - 2 * cornerY

        fontSize = max(self.width() / 5, 10)
        padding = fontSize
        painter.setFont(QFont("Monospace", fontSize))

        painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.translate(0, cornerY)

        for i in range(int(maxSpeed / speedIncrement) * 2 + 1):
            y = int(interpolate(i, 0, 2 * maxSpeed / speedIncrement, padding, gaugeHeight - padding))
            painter.drawLine(fontSize, y, fontSize + self.width() / 8, y)

            if i % numberIncrement == 0:
                painter.drawText(0, y + (fontSize / 2), "{}".format(abs(i - maxSpeed)))

        painter.translate(0, self.height() / 2 - cornerY)

        currentSpeedY = -int(interpolate(clamp(self.value, -maxSpeed, maxSpeed), 0, 2 * maxSpeed / speedIncrement, 0, gaugeHeight - padding))

        if abs(self.value) > maxSpeed:
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))

        painter.drawLine(self.width() * 1.5, 0, self.width() / 3, currentSpeedY)

    def setValue(self, value):
        self.value = value
