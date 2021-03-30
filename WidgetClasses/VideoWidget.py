"""
Text box widget
"""

import PyQt5.QtGui as QtGui
import cv2
from PyQt5.QtWidgets import QLabel, QMenu, QSizePolicy

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from DataHelpers import getValueFromDictionary


class VideoWidget(CustomBaseWidget):
    def __init__(self, tab, name, xPos, yPos, widgetInfo):
        QTWidget = QLabel(tab)
        QTWidget.setObjectName(name)
        super().__init__(QTWidget, xPos, yPos, widgetType=Constants.VIDEO_WINDOW_TYPE)

        dimensions = getValueFromDictionary(widgetInfo, Constants.DIMENSIONS_ATTRIBUTE, "100x100")
        dimensions = dimensions.split("x")
        width = int(float(dimensions[0]))
        height = int(float(dimensions[1]))
        self.source = getValueFromDictionary(widgetInfo, Constants.SOURCE_ATTRIBUTE, "video")

        self.setSize(width, height)
        self.draggable = False

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            return

        if dataPassDict[self.source] is None:
            return

        if type(dataPassDict[self.source]) == int:
            return

        screenWidth = self.QTWidget.parent().size().width()
        screenHeight = self.QTWidget.parent().size().height()

        frame = dataPassDict[self.source]
        height, width, channels = frame.shape
        aspectRatio = float(width) / float(height)
        screenAspectRatio = float(screenWidth) / float(screenHeight)

        # Fix aspect ratio
        if aspectRatio >= screenAspectRatio:
            imageWidth = screenWidth
            imageHeight = int(self.width / aspectRatio)
        else:
            imageHeight = screenHeight
            imageWidth = int(self.height * aspectRatio)

        # If the width isn't a multiple of four, bad things happen
        imageWidth = 4 * round(imageWidth / 4)

        self.setSize(int(imageWidth), int(imageHeight))
        centeredCornerPos = (screenWidth - imageWidth) / 2
        self.setPosition(int(centeredCornerPos), 0)

        # Resize image
        frame = cv2.resize(frame, (int(imageWidth), int(imageHeight)))
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        self.QTWidget.setPixmap(convertToQtFormat)
        self.QTWidget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def rightClickMenu(self, e):
        menu = QMenu()
        awesome = menu.addAction("Whack Patrick")
        menu.move(e.x() + self.x, e.y() + self.y + 90)
        action = menu.exec_()

        if action == awesome:
            print("Patrick has been whacked!!!!!!!!!!!!!!!!!!")

    def setColor(self, color, textColor=None, headerTextColor=None, borderColor=None):
        pass

    def setDraggable(self, draggable):
        pass

    def customXMLStuff(self, tag):
        tag.set(Constants.FULLSCREEN_ATTRIBUTE, "true")
        tag.set(Constants.LOCK_ASPECT_RATIO_ATTRIBUTE, "true")
        tag.set(Constants.DIMENSIONS_ATTRIBUTE, "{0}x{1}".format(int(self.width), int(self.height)))
