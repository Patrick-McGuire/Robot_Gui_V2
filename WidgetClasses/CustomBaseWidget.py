"""
Base class that all our widgets are derived off of
"""


class CustomBaseWidget(object):
    def __init__(self):
        self.QTWidget = None

    def GetTopLevelWidget(self):
        """
        Returns the QT Widget that is the top level for this CustomWidget
        """

        return self.QTWidget
