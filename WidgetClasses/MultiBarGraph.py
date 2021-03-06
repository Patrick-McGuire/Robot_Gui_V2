import xml.etree.ElementTree as ElementTree

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants

from WidgetClasses.QWidgets import SimpleBarGraphWidget, CircleBarGraphWidget


class MultiBarGraph(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        QTWidget = QWidget(tab)
        QTWidget.setObjectName(name)
        self.loaded = False

        super().__init__(QTWidget, x, y, configInfo=widgetInfo, widgetType=Constants.MULTI_GRAPH_TYPE)

        if self.size is None:  # Set a default size
            self.size = 400
        if self.transparent is None:
            self.transparent = False
        self.title = None

        self.BarGraphWidgets = []
        self.Sources = []
        layout = QGridLayout()

        if Constants.CONFIG_ATTRIBUTE in widgetInfo:
            configInfo = widgetInfo[Constants.CONFIG_ATTRIBUTE]
            graphNumber = len(configInfo)
            for i in range(graphNumber):
                config = configInfo[i]
                graphType = config[0]
                source = config[1]
                title = config[2]
                minValue = float(config[3])
                maxValue = float(config[4])
                color = config[5]

                if graphType == "SimpleBarGraph":
                    self.BarGraphWidgets.append(SimpleBarGraphWidget.SimpleBarGraphWidget(title=title, minValue=minValue, maxValue=maxValue, barColor=color))
                elif graphType == "CircleBarGraph":
                    self.BarGraphWidgets.append(CircleBarGraphWidget.CircleBarGraphWidget(title=title, minValue=minValue, maxValue=maxValue, barColor=color))
                else:  # Use simple bar graph as the default
                    self.BarGraphWidgets.append(SimpleBarGraphWidget.SimpleBarGraphWidget(title=title, minValue=minValue, maxValue=maxValue, barColor=color))

                self.Sources.append(source)
                self.BarGraphWidgets[-1].setSize(self.size)
                layout.addWidget(self.BarGraphWidgets[-1], 1, i)
        else:  # Default case launches both types of widgets
            self.BarGraphWidgets.append(SimpleBarGraphWidget.SimpleBarGraphWidget())
            self.BarGraphWidgets[-1].setSize(self.size)
            layout.addWidget(self.BarGraphWidgets[-1], 1, 1)
            self.Sources.append("verticalSpeed")

            self.BarGraphWidgets.append(CircleBarGraphWidget.CircleBarGraphWidget(minValue=0, maxValue=360))
            self.BarGraphWidgets[-1].setSize(self.size)
            layout.addWidget(self.BarGraphWidgets[-1], 1, 2)
            self.Sources.append("roll")

        self.QTWidget.setLayout(layout)
        self.QTWidget.adjustSize()
        self.loaded = True

    def customUpdate(self, dataPassDict):
        for i in range(len(self.BarGraphWidgets)):
            source = self.Sources[i]

            if source in dataPassDict:
                value = float(dataPassDict[source])
            else:
                value = 0

            self.BarGraphWidgets[i].setValue(value)

        self.QTWidget.adjustSize()
        self.QTWidget.update()

    def setColorRGB(self, red, green, blue):
        if self.loaded:
            for widget in self.BarGraphWidgets:
                widget.setTextColor(self.textColor)

        if self.transparent:
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + " color: " + self.textColor + "}")
        else:
            colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
            self.QTWidget.setStyleSheet("QWidget#" + self.QTWidget.objectName() + " {" + colorString + " color: " + self.textColor + "}")

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")

    def customXMLStuff(self, tag):
        pass
        items = []
        for i in range(len(self.BarGraphWidgets)):
            widget = self.BarGraphWidgets[i]
            source = self.Sources[i]

            items.append(ElementTree.SubElement(tag, Constants.LINE_NAME))
            items[-1].set(Constants.TYPE_ATTRIBUTE, widget.getType())
            items[-1].set(Constants.SOURCE_ATTRIBUTE, source)
            items[-1].set(Constants.TITLE_ATTRIBUTE, widget.title)
            items[-1].set(Constants.MIN_ATTRIBUTE, widget.getMin())
            items[-1].set(Constants.MAX_ATTRIBUTE, widget.getMax())
            items[-1].set(Constants.COLOR_ATTRIBUTE, widget.getColor())
