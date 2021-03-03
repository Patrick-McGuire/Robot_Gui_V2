import os
import PyQt5.QtGui as QtGui
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import imutils

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.QWidgets import CompassDisplayWidget


class CompassWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QLabel(tab)
        QTWidget.setObjectName(name)
        self.compassWidget = CompassDisplayWidget.CompassDisplayWidget(QTWidget)

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.COMPASS_TYPE)

        if self.size is None:  # Set a default size
            self.size = 200
        if self.transparent is None:
            self.transparent = True
        self.title = None

        self.setSize(self.size, self.size)
        self.compassWidget.setSize(self.size)

    def customUpdate(self, dataPassDict):
        if self.source not in dataPassDict:
            rotation = 0
        else:
            rotation = -(float(dataPassDict[self.source]) + 90)  # Convert to actual compass heading

        self.compassWidget.setYaw(rotation)

    def setColorRGB(self, red, green, blue):
        if self.transparent:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        else:
            colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + colorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")
