"""
Base class that all our widgets are derived off of
"""


class CustomBaseWidget(object):
    def __init__(self, QTWidget, x, y):
        self.QTWidget = QTWidget
        self.QTWidget.move(x, y)

        self.x = x
        self.y = y

    def GetTopLevelWidget(self):
        """Returns the QT Widget that is the top level for this CustomWidget"""

        return self.QTWidget

    def Update(self, dataPassDict):
        pass
