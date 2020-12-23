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

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.COMPASS_TYPE)

        self.size = int(widgetInfo["size"])
        self.source = str(widgetInfo[Constants.SOURCE_ATTRIBUTE])

        self.setSize(self.size, self.size)
        self.arrow.setGeometry(0, 0, self.size, self.size)

        dirName = os.path.dirname(__file__)
        dirName = os.path.abspath(os.path.join(dirName, ".."))

        img = cv2.resize(cv2.imread("{}/Assets/compass.png".format(dirName), cv2.IMREAD_UNCHANGED), (self.size, self.size))
        convertToQtFormat = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_ARGB32)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.QTWidget.setPixmap(pixmap)

        self.arrowImg = cv2.resize(cv2.imread("{}/Assets/arrow.png".format(dirName), cv2.IMREAD_UNCHANGED)[900:2100, 900:2100], (self.size, int(self.size / 2)))

        self.setColor("grey")

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

    def setColorRGB(self, red, green, blue):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        if max(red, green, blue) > 127:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: black}")
            self.arrow.setStyleSheet("color: black")
        else:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid black; " + colorString + " color: white}")
            self.arrow.setStyleSheet("color: black")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
        self.arrow.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set(Constants.SOURCE_ATTRIBUTE, self.source)
        tag.set(Constants.SIZE_ATTRIBUTE, str(self.size))
