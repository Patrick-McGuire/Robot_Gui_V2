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


class CircleBarGraphWidget(QLabel):
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

        self.setGeometry(0, 0, size, size)
        self.setMinimumWidth(size)
        self.setMinimumHeight(size)

    def paintEvent(self, e):
        painter = QPainter(self)  # Grey background

        fontSize = int(self.width() * 0.1)
        padding = 4
        painter.setPen(QPen(self.textColor, 1, Qt.SolidLine))
        painter.setFont(QFont("Monospace", fontSize))
        fontHeight = int(fontSize * 1.5)

        valueText = str(self.value)[0:6]
        painter.drawText(QRect(0, 0, self.width(), self.height() * 0.9), Qt.AlignCenter, valueText)

        painter.setFont(QFont("Monospace", fontSize / 2))
        painter.drawText(QRect(0, (self.height() * 0.9 / 2) + fontHeight / 2 + padding, self.width(), fontHeight / 2), Qt.AlignCenter, self.title)

        theta = clamp(interpolate(self.value, self.minValue, self.maxValue, 0, 360 * 16), 0, 360 * 16)
        barPadding = 20

        painter.setPen(QPen(self.barColor, 30, Qt.SolidLine))
        painter.translate(0, self.height())
        painter.rotate(-90)

        painter.drawArc(barPadding, barPadding, self.width() - 2 * barPadding, self.height() - 2 * barPadding, 0, -theta)

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
        return "CircleBarGraph"

    def getLimits(self):
        return [self.minValue, self.maxValue]

    def getMin(self):
        return str(self.minValue)

    def getMax(self):
        return str(self.maxValue)

    def getColor(self):
        colorString = "rgb({0},{1},{2})".format(self.barColor.red(), self.barColor.green(), self.barColor.blue())
        return colorString
