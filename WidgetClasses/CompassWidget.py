import PyQt5.QtGui as QtGui
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import imutils

from .CustomBaseWidget import CustomBaseWidget


class CompassWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, size):
        QTWidget = QLabel(tab)
        super().__init__(QTWidget, x, y)
        self.QTWidget.setObjectName(name)
        self.size = size
        self.arrow = QLabel(self.QTWidget)

        self.setSize(self.size, self.size)
        self.arrow.setGeometry(0, 0, self.size, self.size)

        img = cv2.resize(cv2.imread("Assets/compass.png", cv2.IMREAD_UNCHANGED), (self.size, self.size))
        convertToQtFormat = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_ARGB32)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.QTWidget.setPixmap(pixmap)

        self.arrowImg = cv2.resize(cv2.imread("Assets/arrow.png", cv2.IMREAD_UNCHANGED)[900:2100, 900:2100], (self.size, int(self.size / 2)))

        self.a = 0

    def update(self, dataPassDict):
        self.a = self.a + 1
        img = imutils.rotate(self.arrowImg, self.a)
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
