"""
Frame rate counter

Actually doesn't count framerate right now

Just used to keep the gui updating if nothing else is drawing
"""

import time

from PyQt5.QtWidgets import QLabel

from .CustomBaseWidget import CustomBaseWidget


class FrameRateCounter(CustomBaseWidget):
    def __init__(self, tab, x, y):
        super().__init__(QLabel(tab), x, y)
        self.QTWidget.show()
        self.xBuffer = 0
        self.yBuffer = 0

    def update(self, dataPassDict, listOfWidgets):
        outString = str(time.time())

        self.QTWidget.setText(outString)
        self.QTWidget.adjustSize()

    def getXMLStuff(self, item):
        """We don't want this widget saved out"""
        return
