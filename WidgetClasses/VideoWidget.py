"""
Text box widget
"""

import PyQt5.QtGui as QtGui
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMenu

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class VideoWidget(CustomBaseWidget):
    def __init__(self, tab, xPos, yPos, widgetInfo):
        QTWidget = QLabel(tab)
        super().__init__(QTWidget, xPos, yPos)

        width = int(float(widgetInfo[Constants.DIMENSIONS_ATTRIBUTE].split("x")[0]))
        height = int(float(widgetInfo[Constants.DIMENSIONS_ATTRIBUTE].split("x")[1]))

        self.setSize(width, height)

    def customUpdate(self, dataPassDict):
        if "image" not in dataPassDict:
            return

        frame = dataPassDict["image"]

        height, width, channels = frame.shape
        aspectRatio = float(width) / float(height)
        widgetAspectRatio = float(self.width) / float(self.height)

        # Fix aspect ratio
        if aspectRatio >= widgetAspectRatio:
            imageWidth = self.width
            imageHeight = int(self.width / aspectRatio)
        else:
            imageHeight = self.height
            imageWidth = int(self.height * aspectRatio)

        if imageWidth == self.width + 1:
            imageWidth = self.width

        # Resize image
        frame = cv2.resize(frame, (int(imageWidth), int(imageHeight)))
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.QTWidget.setPixmap(pixmap)

    def rightClickMenu(self, e):
        menu = QMenu()
        awesome = menu.addAction("Whack Patrick")
        menu.move(e.x() + self.x, e.y() + self.y + 90)
        action = menu.exec_()

        if action == awesome:
            print("Patrick has been whacked!!!!!!!!!!!!!!!!!!")

    def setColor(self, color):
        pass
