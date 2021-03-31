from PyQt5.QtWidgets import QWidget, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.QWidgets import SimpleMapWidget
from DataHelpers import getValueFromDictionary


class MapWidget(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QWidget(tab)
        QTWidget.setObjectName(name)
        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.MAP_TYPE)

        if self.size is None:  # Set a default size
            self.size = 400
        if self.transparent is None:
            self.transparent = False
        self.source = None
        self.font = None
        self.fontSize = None

        if self.title is None:
            self.title = name

        self.XSource = getValueFromDictionary(widgetInfo, "XSource", "x_position_global")
        self.YSource = getValueFromDictionary(widgetInfo, "YSource", "y_position_global")
        self.pointsToKeep = int(getValueFromDictionary(widgetInfo, "PointsToKeep", "200"))
        self.pointSpacing = float(getValueFromDictionary(widgetInfo, "PointSpacing", "0.1"))
        self.fullScreen = getValueFromDictionary(widgetInfo, Constants.FULLSCREEN_ATTRIBUTE, "false").lower() == "true"

        self.SimpleMapWidget = SimpleMapWidget.SimpleMapWidget(pointsToKeep=self.pointsToKeep, pointSpacing=self.pointSpacing)

        layout = QGridLayout()
        layout.addWidget(self.SimpleMapWidget)
        self.QTWidget.setLayout(layout)

        if not self.fullScreen:
            self.SimpleMapWidget.setSize(self.size)
        else:
            self.transparent = True
            self.SimpleMapWidget.setSize(10)

        self.QTWidget.adjustSize()

    def customUpdate(self, dataPassDict):
        x = getValueFromDictionary(dataPassDict, self.XSource, 0)
        y = getValueFromDictionary(dataPassDict, self.YSource, 0)

        screenWidth = self.QTWidget.parent().size().width()
        screenHeight = self.QTWidget.parent().size().height()
        screenSize = min(screenWidth, screenHeight)

        if self.fullScreen:
            self.setSize(screenSize, screenSize)
            centeredCornerPos = (screenWidth - self.QTWidget.width()) / 2
            self.setPosition(int(centeredCornerPos), 0)
            self.draggable = False

        self.SimpleMapWidget.setXY(x, y)

        if not self.hidden:
            self.QTWidget.adjustSize()
            self.QTWidget.update()

    def setColorRGB(self, red, green, blue):

        if self.transparent:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        else:
            colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {border: 1px solid " + self.borderColor + "; " + colorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        tag.set("XSource", self.XSource)
        tag.set("YSource", self.YSource)
        tag.set("PointsToKeep", str(self.pointsToKeep))
        tag.set("PointSpacing", str(self.pointSpacing))
        tag.set(Constants.FULLSCREEN_ATTRIBUTE, str(self.fullScreen))
