"""
Text box widget
"""
from PyQt5.QtWidgets import QComboBox

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class SimpleDropDown(CustomBaseWidget):
    def __init__(self, tab, xPos, yPos):
        QTWidget = QComboBox(tab)

        super().__init__(QTWidget, xPos, yPos, hasReturnValue=True, returnKey="drop_down_one", widgetType=Constants.SIMPLE_DROP_DOWN_TYPE)

        self.setMenuItems()

    def setMenuItems(self):
        menuList = ["thing1", "thing2", "patrick"]
        self.QTWidget.clear()
        self.QTWidget.addItems(menuList)

    def getCurrentText(self):
        return self.QTWidget.currentText()

    def getData(self):
        return self.getCurrentText()

    def setColorRGB(self, red: int, green: int, blue: int):
        colorString = "background: rgb({0}, {1}, {2});".format(red, green, blue)

        if max(red, green, blue) > 127:
            self.QTWidget.setStyleSheet(colorString + " color: black")
        else:
            self.QTWidget.setStyleSheet(colorString + " color: white")
