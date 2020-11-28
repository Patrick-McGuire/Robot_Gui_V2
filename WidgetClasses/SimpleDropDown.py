"""
Text box widget
"""
from PyQt5.QtWidgets import QComboBox

from .CustomBaseWidget import CustomBaseWidget


class SimpleDropDown(CustomBaseWidget):
    def __init__(self, tab, xPos, yPos):
        QTWidget = QComboBox(tab)

        super().__init__(QTWidget, xPos, yPos, hasReturnValue=True, returnKey="drop_down_one")

        self.setMenuItems()

    def setMenuItems(self):
        menuList = ["thing1", "thing2", "patrick"]
        self.QTWidget.clear()
        self.QTWidget.addItems(menuList)

    def getCurrentText(self):
        return self.QTWidget.currentText()

    def getData(self):
        return self.getCurrentText()
