"""
Text box widget
"""

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon, QImage, QPixmap

import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

import cv2

from .CustomBaseWidget import CustomBaseWidget


class VideoWidget(CustomBaseWidget):
    def __init__(self, tab, xPos, yPos):
        QTWidget = QLabel(tab)
        super().__init__(QTWidget, xPos, yPos)

        self.width = 2000
        self.height = 2000

    def update(self, dataPassDict):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        if ret:
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
            convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
            pixmap = QPixmap(convertToQtFormat)
            resizeImage = pixmap.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
            self.QTWidget.setPixmap(resizeImage)
