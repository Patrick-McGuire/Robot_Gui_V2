from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint


class AltitudeSpeedIndicatorWidget(QLabel):
    def __init__(self, parentWidget: QWidget = None, leftOriented=True):
        super().__init__(parentWidget)

        self.size = 200

        self.spacing = 20  # Delta Value between lines
        self.onScreenSpacing = 20  # Delta Pixels between lines
        self.value = 0

        self.leftOriented = leftOriented

    def setSize(self, size):
        # TODO: Use the QWidget size functions instead of this sketchy one
        self.size = size

        self.setGeometry(0, 0, size / 4, size)
        self.setMinimumWidth(size / 4)
        self.setMinimumHeight(size)

    def paintEvent(self, e):
        painter = QPainter(self)  # Grey background
        painter.setPen(QPen(QColor(50, 50, 50), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(50, 50, 50), Qt.SolidPattern))
        painter.drawRect(0, 0, self.width(), self.height())

        lineWidth = self.height() / 100

        painter.translate(int(self.width() / 2), int(self.height() / 2))  # Set our coordinate system to be centered on the widget
        painter.setPen(QPen(Qt.white, lineWidth, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        scaleFactor = float(self.onScreenSpacing) / float(self.spacing)

        maxValueToDraw = int(self.value + (self.height() / 2) * scaleFactor)
        minValueToDraw = int(self.value - (self.height() / 2) * scaleFactor)

        maxValueToDraw = self.spacing * round((maxValueToDraw / self.spacing) + 2)
        minValueToDraw = self.spacing * round(minValueToDraw / self.spacing)

        shortLength = 10
        longLength = 20
        fontSize = 10

        startX = int(self.width() / 2)
        endX = int(self.width() / 2) - shortLength

        if self.leftOriented:
            startX = -startX
            endX = -endX

        for i in range(minValueToDraw, maxValueToDraw, self.spacing):
            lineYPosition = (self.value - i) * scaleFactor

            painter.drawLine(startX, lineYPosition, endX, lineYPosition)

            painter.setFont(QFont("Monospace", fontSize))

            if self.leftOriented:
                painter.drawText(endX + 5, lineYPosition + int(fontSize / 2), "{}".format(abs(i)))
            else:
                painter.drawText(endX - 5 - (3 * (fontSize - 2)), lineYPosition + int(fontSize / 2), "{:>3}".format(abs(i)))

    def setValue(self, value):
        self.value = value
