"""
Base class that all our widgets are derived off of
"""

from PyQt5.QtWidgets import QWidget, QMenu
from PyQt5.QtCore import Qt


class CustomBaseWidget(object):
    def __init__(self, QTWidget: QWidget, x: float, y: float, hasReturnValue: bool = False, returnKey: str = None):
        self.QTWidget = QTWidget
        self.QTWidget.move(x, y)
        self.QTWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.QTWidget.customContextMenuRequested.connect(self.rightClickMenu)

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

    def setSize(self, width, height):
        self.QTWidget.setMinimumWidth(width)
        self.QTWidget.setMaximumWidth(width)
        self.QTWidget.setMinimumHeight(height)
        self.QTWidget.setMaximumHeight(height)

        self.width = width
        self.height = height

    def rightClickMenu(self, e):
        colorMenu = QMenu("Set color")
        whiteAction = colorMenu.addAction("white")
        blueAction = colorMenu.addAction("blue")
        defaultAction = colorMenu.addAction("default")

        menu = QMenu()
        menu.addMenu(colorMenu)
        awesome = menu.addAction("Whack Patrick")
        menu.move(e.x() + self.x, e.y() + self.y + 90)
        action = menu.exec_()

        if action == whiteAction:
            self.setColor("white")
        if action == defaultAction:
            self.setColor("default")
        elif action == blueAction:
            self.setColor("blue")
        elif action == awesome:
            print("Patrick has been whacked!!!!!!!!!!!!!!!!!!")

    def setColor(self, color):
        if color == "white":
            self.QTWidget.setStyleSheet("border: 1px solid black; background: rgb(255, 255, 255); color: black")
        elif color == "blue":
            self.QTWidget.setStyleSheet("border: 1px solid black; background: rgb(0, 0, 100); color: white")
        elif color == "default":
            self.QTWidget.setStyleSheet("color: black")
        else:
            self.QTWidget.setStyleSheet("color: black")

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
        if self.x - self.xBuffer <= x <= (self.x + self.width + self.xBuffer):
            if (self.y + 30 - self.yBuffer) <= y <= (self.y + self.height + 30 + self.yBuffer):
                return True
        return False

    def setPosition(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.QTWidget.move(self.x, self.y)
