from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRect


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


class SimpleBarGraphWidget(QLabel):
    def __init__(self, parentWidget: QWidget = None, title="Title", minValue=0, maxValue=100, size=200, barColor=None):
        super().__init__(parentWidget)
        self.size = size
        self.value = 0
        self.title = title

        self.minValue = minValue
        self.maxValue = maxValue

        if barColor is not None:
            [red, green, blue] = [int(float(i)) for i in barColor.split("(")[1].split(")")[0].split(",")]
            self.barColor = QColor(red, green, blue)
        else:
            self.barColor = QColor(50, 50, 255)

        self.textColor = QColor(255, 255, 255)

        self.setAlignment(Qt.AlignCenter)

    def setSize(self, size):
        # TODO: Use the QWidget size functions instead of this sketchy one
        self.size = size

        width = size / 3

        self.setGeometry(0, 0, width, size)
        self.setMinimumWidth(width)
        self.setMinimumHeight(size)

    def paintEvent(self, e):
        painter = QPainter(self)  # Grey background

        fontSize = int(self.width() * 0.15)
        padding = 4
        painter.setPen(QPen(self.textColor, 1, Qt.SolidLine))
        painter.setFont(QFont("Monospace", fontSize))
        fontHeight = int(fontSize * 1.5)

        valueText = str(self.value)[0:6]

        painter.drawText(QRect(0, padding, self.width(), fontHeight), Qt.AlignCenter, self.title)
        painter.drawText(QRect(0, self.height() - fontHeight - padding, self.width(), fontHeight), Qt.AlignCenter, valueText)

        painter.setPen(QPen(QColor(100, 100, 100), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(50, 50, 50), Qt.SolidPattern))

        topY = 2 * padding + fontHeight
        rectangleHeight = self.height() - 2 * topY
        startX = self.width() * 0.1
        rectangleWidth = self.width() - 2 * startX

        painter.translate(0, topY + rectangleHeight)

        painter.drawRect(startX, 0, rectangleWidth, -rectangleHeight)

        painter.setPen(QPen(self.barColor, 0, Qt.SolidLine))
        painter.setBrush(QBrush(self.barColor, Qt.SolidPattern))

        barHeight = clamp(interpolate(self.value, self.minValue, self.maxValue, 0, rectangleHeight), 0, rectangleHeight)
        painter.drawRect(startX, 0, rectangleWidth, -barHeight)

    def setValue(self, value):
        self.value = value

    def setTextColor(self, textColor: str):
        if "rgb" in textColor:
            [red, green, blue] = [int(float(i)) for i in textColor.split("(")[1].split(")")[0].split(",")]
            self.textColor = QColor(red, green, blue)
        else:
            self.textColor = QColor(textColor)

    @staticmethod
    def getType():
        return "SimpleBarGraph"

    def getLimits(self):
        return [self.minValue, self.maxValue]

    def getMin(self):
        return str(self.minValue)

    def getMax(self):
        return str(self.maxValue)

    def getColor(self):
        colorString = "rgb({0},{1},{2})".format(self.barColor.red(), self.barColor.green(), self.barColor.blue())
        return colorString
