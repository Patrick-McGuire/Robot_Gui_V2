"""
Base class that all our widgets are derived off of
"""


class CustomBaseWidget(object):
    def __init__(self, QTWidget, x, y):
        self.QTWidget = QTWidget
        self.QTWidget.move(x, y)

        self.x = x
        self.y = y
        self.width = 50
        self.height = 50


    def getTopLevelWidget(self):
        """Returns the QT Widget that is the top level for this CustomWidget"""

        return self.QTWidget

    def update(self, dataPassDict):
        pass

    def isPointInWidget(self, x, y):
        self.width = float(self.QTWidget.minimumWidth())
        self.height = float(self.QTWidget.minimumHeight())

        if self.x <= x <= (self.x + self.width):
            if (self.y + 30) <= y <= (self.y + self.height + 30):
                return True
        return False

    def setPosition(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.QTWidget.move(self.x, self.y)
