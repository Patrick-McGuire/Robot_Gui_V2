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
                if Constants.VIDEO_WINDOW_TYPE in widget.type or Constants.MAP_TYPE in widget.type:
                    if widget.fullScreen:  # We only want the Maps and Video screens that are full screen
                        widgetNames.append(widget.getTitle())

                        if widget.getTitle() == self.activeWidget:
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
