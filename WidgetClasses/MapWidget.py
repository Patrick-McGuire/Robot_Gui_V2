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
        self.title = None
        self.source = None

        self.XSource = getValueFromDictionary(widgetInfo, "XSource", "x_position_global")
        self.YSource = getValueFromDictionary(widgetInfo, "YSource", "y_position_global")
        self.pointsToKeep = int(getValueFromDictionary(widgetInfo, "PointsToKeep", "200"))
        self.pointSpacing = float(getValueFromDictionary(widgetInfo, "PointSpacing", "0.1"))

        self.SimpleMapWidget = SimpleMapWidget.SimpleMapWidget(pointsToKeep=self.pointsToKeep, pointSpacing=self.pointSpacing)

        layout = QGridLayout()
        layout.addWidget(self.SimpleMapWidget)
        self.QTWidget.setLayout(layout)

        self.SimpleMapWidget.setSize(self.size)

        self.QTWidget.adjustSize()

    def customUpdate(self, dataPassDict):
        x = getValueFromDictionary(dataPassDict, self.XSource, 0)
        y = getValueFromDictionary(dataPassDict, self.YSource, 0)

        self.SimpleMapWidget.setXY(x, y)

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
