from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon, QColor, QFont, QRegion
from PyQt5.QtCore import Qt, QPoint


class AltitudeSpeedIndicatorWidget(QLabel):
    def __init__(self, parentWidget: QWidget = None, leftOriented=True, onScreenSpacingScale=1):
        super().__init__(parentWidget)

        self.size = 200

        self.textSpacing = 1  # Delta Value between lines with text
        self.onScreenSpacingScale = onScreenSpacingScale * 10  # Delta Pixels between lines
        self.value = 0

        self.leftOriented = leftOriented

    def setSize(self, size):
        # TODO: Use the QWidget size functions instead of this sketchy one
        self.size = size

        self.setGeometry(0, 0, size / 4, size)
        self.setMinimumWidth(size / 4)
        self.setMinimumHeight(size)

    def paintEvent(self, e):
        onScreenSpacing = self.height() / (100 / self.onScreenSpacingScale)

        painter = QPainter(self)  # Grey background
        painter.setPen(QPen(QColor(50, 50, 50), 0, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(50, 50, 50), Qt.SolidPattern))
        painter.drawRect(0, 0, self.width(), self.height())

        lineWidth = self.height() / 100

        painter.translate(int(self.width() / 2), int(self.height() / 2))  # Set our coordinate system to be centered on the widget
        painter.setPen(QPen(Qt.white, lineWidth, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        scaleFactor = float(onScreenSpacing) / float(self.textSpacing)  # Roughly correlated to pixels between lines

        maxValueToDraw = int(self.value + (self.height() / 2) / scaleFactor)
        minValueToDraw = int(self.value - (self.height() / 2) / scaleFactor)

        maxValueToDraw = self.textSpacing * round((maxValueToDraw / self.textSpacing) + 1)
        minValueToDraw = self.textSpacing * round((minValueToDraw / self.textSpacing) - 1)

        shortLength = 10
        fontSize = max(self.width() / 5, 10)

        startX = int(self.width() / 2)
        endX = int(self.width() / 2) - shortLength

        if self.leftOriented:
            startX = -startX
            endX = -endX

        linesBetweenText = int(scaleFactor / 15)
        for i in range(int(linesBetweenText * minValueToDraw), int(linesBetweenText * maxValueToDraw), self.textSpacing):
            lineYPosition = (self.value - (i / linesBetweenText)) * scaleFactor

            painter.drawLine(startX, lineYPosition, endX, lineYPosition)

            painter.setFont(QFont("Monospace", fontSize))

            if i % 2 == 0:
                if self.leftOriented:
                    painter.drawText(endX + 5, lineYPosition + int(fontSize / 2), "{}".format((i / linesBetweenText)))
                else:
                    painter.drawText(endX - 5 - (3 * (fontSize - 2)), lineYPosition + int(fontSize / 2), "{:>3}".format((i / linesBetweenText)))

        pointerCornerX = int(self.width() / 5)
        pointerHeight = int(self.height() / 20)

        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        if self.leftOriented:
            points = [
                QPoint(-pointerCornerX, pointerHeight),
                QPoint(self.width() / 2, pointerHeight),
                QPoint(self.width() / 2, -pointerHeight),
                QPoint(-pointerCornerX, -pointerHeight),
                QPoint(-self.width() / 2, 0),
            ]
        else:
            points = [
                QPoint(pointerCornerX, pointerHeight),
                QPoint(-self.width() / 2, pointerHeight),
                QPoint(-self.width() / 2, -pointerHeight),
                QPoint(pointerCornerX, -pointerHeight),
                QPoint(self.width() / 2, 0),
            ]
        poly = QPolygon(points)
        painter.drawPolygon(poly)

        if self.leftOriented:
            painter.drawText(int(-1.5 * (fontSize - 2)), int(fontSize / 2), "{}".format(self.value))
        else:
            painter.drawText(int(-2.5 * (fontSize - 2)), int(fontSize / 2), "{}".format(self.value))

    def setValue(self, value):
        self.value = value
