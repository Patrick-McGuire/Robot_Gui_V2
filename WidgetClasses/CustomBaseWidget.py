"""
Base class that all our widgets are derived off of
"""

from PyQt5.QtWidgets import QWidget


class CustomBaseWidget(object):
    def __init__(self, QTWidget: QWidget, x: float, y: float, hasReturnValue: bool = False, returnKey: str = None):
        self.QTWidget = QTWidget
        self.QTWidget.move(x, y)
        QTWidget.setToolTip("Holy shit this works")

        if hasReturnValue and returnKey is None:
            print("No ReturnDataDict key specified for a widget.  This widget won't return data")
            self.hasReturnValue = False
        else:
            self.hasReturnValue = hasReturnValue

        self.returnKey = returnKey

        self.x = x
        self.y = y
        self.xBuffer = 20
        self.yBuffer = 20
        self.width = 50
        self.height = 50

    def returnsData(self):
        """Returns true if this widget has data to return"""
        return self.hasReturnValue

    def getTopLevelWidget(self):
        """Returns the QT Widget that is the top level for this CustomWidget"""
        return self.QTWidget

    def update(self, dataPassDict):
        """Update the widget.  Should be overwritten."""
        pass

    def getData(self):
        """Function to return data from a widget.  Should be overwritten"""
        return 0

    def getReturnKey(self):
        """Returns the dictionary key to put the return data into"""
        return self.returnKey

    def isPointInWidget(self, x, y):
        if self.x-self.xBuffer <= x <= (self.x + self.width+self.xBuffer):
            if (self.y + 30-self.yBuffer) <= y <= (self.y + self.height + 30+self.yBuffer):
                return True
        return False

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.QTWidget.move(x, y)
