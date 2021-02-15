import os
import PyQt5.QtGui as QtGui
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import imutils

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class CompassWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QLabel(tab)
        QTWidget.setObjectName(name)
        self.arrow = QLabel(QTWidget)
        self.imageLoaded = False

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.COMPASS_TYPE)

        if self.size is None:  # Set a default size
            self.size = 200

        self.setSize(self.size, self.size)
        self.arrow.setGeometry(0, 0, self.size, self.size)

        dirName = os.path.dirname(__file__)
        dirName = os.path.abspath(os.path.join(dirName, ".."))
        self.img = cv2.imread("{}/Assets/compass.png".format(dirName), cv2.IMREAD_UNCHANGED)
        self.arrowImg = cv2.resize(cv2.imread("{}/Assets/arrow.png".format(dirName), cv2.IMREAD_UNCHANGED)[900:2100, 900:2100], (self.size, int(self.size / 2)))
        self.imageColor = "black"

        self.imageLoaded = True
        self.setBackground()

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            rotation = 0
        else:
            rotation = -(float(dataPassDict[self.source]) + 90)  # Convert to actual compass heading

        img = imutils.rotate(self.arrowImg, rotation)
        convertToQtFormat = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_ARGB32)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.arrow.setPixmap(pixmap)
        self.arrow.setStyleSheet("color: black")

    def setBackground(self):
        if not self.imageLoaded:
            return

        img = cv2.resize(self.img, (self.size, self.size))
        [red, green, blue] = self.getRGBFromColor(self.imageColor)

        for i in img:  # Change the color of the whole image
            for j in i:
                j[0] = red
                j[1] = green
                j[2] = blue

        convertToQtFormat = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_ARGB32)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.QTWidget.setPixmap(pixmap)

    def setColorRGB(self, red, green, blue):
        # colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
        # self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + colorString + " color: " + self.textColor + "}")

        self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        self.arrow.setStyleSheet("color: " + self.textColor)

        if max(red, green, blue) > 127:
            self.imageColor = "black"
        else:
            self.imageColor = "white"
        self.setBackground()

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.arrow.setStyleSheet("color: black")
        self.imageColor = "black"
        self.setBackground()
