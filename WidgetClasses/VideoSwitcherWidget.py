"""
Text box widget
"""
from PyQt5.QtWidgets import QComboBox

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants
from typing import List


class VideoSwitcherWidget(CustomBaseWidget):
    def __init__(self, tab, name, xPos, yPos, widgetInfo):
        QTWidget = QComboBox(tab)

        super().__init__(QTWidget, xPos, yPos, hasReturnValue=True, returnKey="active_video", widgetType=Constants.VIDEO_SWITCH_TYPE)

        self.widgetOptions = []
        self.activeWidget = ""

    def customUpdate(self, dataPassDict):
        self.activeWidget = self.getCurrentText()

    def setWidgetList(self, listOfWidgets: List[CustomBaseWidget]):
        widgetNames = []
        for widget in listOfWidgets:
            if widget.getTabName() == self.getTabName():
                if "Video" in widget.getName() or "Map" in widget.getName():
                    widgetNames.append(widget.getName())

                    if widget.getName() == self.activeWidget:
                        widget.show()
                    else:
                        widget.hide()

        if widgetNames != self.widgetOptions:
            self.QTWidget.clear()
            self.widgetOptions = widgetNames
            self.QTWidget.addItems(self.widgetOptions)
            self.QTWidget.adjustSize()

    def getCurrentText(self):
        return self.QTWidget.currentText()

    def getData(self):
        return self.activeWidget

    def setColorRGB(self, red: int, green: int, blue: int):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)
        self.QTWidget.setStyleSheet(colorString + " color: " + self.headerTextColor)
