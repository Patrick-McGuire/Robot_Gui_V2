import imutils
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui


class BasicImageDisplay(object):
    def __init__(self, rootWidget: QLabel, image, targetWidth, x=None, y=None):
        windowWidth = rootWidget.width()
        windowHeight = rootWidget.height()

        self.image = imutils.resize(image, width=int(targetWidth))
        height, width, channels = self.image.shape

        if x is None:
            xOffset = (windowWidth - width) / 2
        else:
            xOffset = x

        if y is None:
            yOffset = (windowHeight - height) / 2
        else:
            yOffset = y

        self.imageWidget = QLabel(rootWidget)
        self.imageWidget.setGeometry(xOffset, yOffset, width, height)

        convertToQtFormat = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_ARGB32)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.imageWidget.setPixmap(pixmap)

    def setRotation(self, theta):
        img = imutils.rotate(self.image, theta)
        convertToQtFormat = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_ARGB32)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        self.imageWidget.setPixmap(pixmap)
