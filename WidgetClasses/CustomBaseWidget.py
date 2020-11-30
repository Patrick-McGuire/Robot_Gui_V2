"""
Base class that all our widgets are derived off of
"""

import random
import webcolors

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMenu
from PyQt5.QtGui import QFont

from Constants import Constants


def convertNameToRGB(name: str):
    try:
        rgb = webcolors.name_to_rgb(name.lower().replace(" ", ""))
        return [rgb.red, rgb.green, rgb.blue]
    except ValueError:
        return False


class CustomBaseWidget(object):
    def __init__(self, QTWidget: QWidget, x: float, y: float, hasReturnValue: bool = False, returnKey: str = None, configInfo=None):
        self.QTWidget = QTWidget
        self.QTWidget.move(x, y)
        self.QTWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.QTWidget.customContextMenuRequested.connect(self.rightClickMenu)
        self.tabName = self.QTWidget.parent().objectName()

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
        self.draggable = True

        # Generic parameters that many widgets might need
        self.borderWidth = 1
        self.font = "Arial"
        self.fontSize = 12
        self.hidden = False

        if configInfo is not None:
            if Constants.BORDER_WIDTH_ATTRIBUTE in configInfo:
                self.borderWidth = int(configInfo[Constants.BORDER_WIDTH_ATTRIBUTE])
            if Constants.FONT_ATTRIBUTE in configInfo:
                self.font = configInfo[Constants.FONT_ATTRIBUTE]
            if Constants.FONT_SIZE_ATTRIBUTE in configInfo:
                self.fontSize = int(configInfo[Constants.FONT_SIZE_ATTRIBUTE])
            if Constants.BACKGROUND_ATTRIBUTE in configInfo:
                self.setColor(configInfo[Constants.BACKGROUND_ATTRIBUTE])

        self.QTWidget.setFont(QFont(self.font, self.fontSize))

    def setSize(self, width, height):
        self.QTWidget.setMinimumWidth(width)
        self.QTWidget.setMaximumWidth(width)
        self.QTWidget.setMinimumHeight(height)
        self.QTWidget.setMaximumHeight(height)

        self.width = width
        self.height = height

    def rightClickMenu(self, e):
        colorMenu = QMenu("Set color")
        whiteAction = colorMenu.addAction("White")
        blueAction = colorMenu.addAction("Blue")
        greyAction = colorMenu.addAction("Grey")
        defaultAction = colorMenu.addAction("Default")

        menu = QMenu()
        menu.addMenu(colorMenu)
        menu.addSeparator()
        menu.addAction("Enable dragging", lambda draggable=True: self.setDraggable(draggable))
        menu.addAction("Disable dragging", lambda draggable=False: self.setDraggable(draggable))
        awesome = menu.addAction("Whack Patrick", lambda x=random.random() * 1500, y=random.random() * 1000: self.setPosition(x, y))  # This is silly
        menu.move(e.x() + self.x, e.y() + self.y + 90)
        action = menu.exec_()

        if action == whiteAction:
            self.setColor("white")
        if action == defaultAction:
            self.setColor("default")
        elif action == blueAction:
            self.setColor("blue")
        elif action == greyAction:
            self.setColor("grey")
        elif action == awesome:
            print("Patrick has been whacked!!!!!!!!!!!!!!!!!!")

    def setColor(self, color):
        color = color.replace("Grey", "Gray")
        color = color.replace("grey", "gray")

        if color == "white":
            self.setColorRGB(255, 255, 255)
        elif color == "blue":
            self.setColorRGB(0, 0, 100)
        elif color == "grey" or color == "gray":
            self.setColorRGB(50, 50, 50)
        elif color == "default":
            self.setDefaultAppearance()
        elif "rgb" in color:
            [red, green, blue] = color.split("[")[1].split("]")[0].split(",")
            self.setColorRGB(int(float(red)), int(float(green)), int(float(blue)))  # Going to float then string fixes issues if the number is 0.0 or similar
        elif convertNameToRGB(color):
            rgb = convertNameToRGB(color)
            self.setColorRGB(rgb[0], rgb[1], rgb[2])
        else:
            self.QTWidget.setStyleSheet("color: black")

    def setColorRGB(self, red: int, green: int, blue: int):
        if max(red, green, blue) > 150:
            self.QTWidget.setStyleSheet("border: {3}px solid black; background: rgb({0}, {1}, {2}); color: black".format(red, green, blue, self.borderWidth))
        else:
            self.QTWidget.setStyleSheet("border: {3}px solid black; background: rgb({0}, {1}, {2}); color: white".format(red, green, blue, self.borderWidth))

    def setDefaultAppearance(self):
        self.QTWidget.setStyleSheet("color: black")

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def setDraggable(self, draggable):
        self.draggable = draggable

    def isDraggable(self):
        return self.draggable

    def returnsData(self):
        """Returns true if this widget has data to return"""
        return self.hasReturnValue

    def getTopLevelWidget(self):
        """Returns the QT Widget that is the top level for this CustomWidget"""
        return self.QTWidget

    def update(self, dataPassDict):
        """
        Code that has to run every update for every widget.  DON'T OVERWRITE THIS ONE, OVERWRITE customUpdate()
        NEEDS TO BE CALLED FROM THE GUI THREAD WITH A QTIMER!!!
        """

        # Hide/show the widget
        # Needs to run here for thread reasons
        if self.QTWidget.isHidden() != self.hidden:
            self.QTWidget.setHidden(self.hidden)

        # Run the custom update code
        self.customUpdate(dataPassDict)

        # Update the size
        self.width = float(self.QTWidget.size().width())
        self.height = float(self.QTWidget.size().height())

    def customUpdate(self, dataPassDict):
        """Update the widget.  Should be overwritten to add custom functionality"""
        pass

    def getData(self):
        """Function to return data from a widget.  Should be overwritten"""
        return 0

    def getReturnKey(self):
        """Returns the dictionary key to put the return data into"""
        return self.returnKey

    def getTabName(self):
        return self.tabName

    def isPointInWidget(self, x, y):
        if self.x - self.xBuffer <= x <= (self.x + self.width + self.xBuffer):
            if (self.y + 50 - self.yBuffer) <= y <= (self.y + self.height + 50 + self.yBuffer):
                return True
        return False

    def setPosition(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.QTWidget.move(self.x, self.y)
