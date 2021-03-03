"""
Base class that all our widgets are derived off of
"""

import random
import webcolors
import copy

import xml.etree.ElementTree as ElementTree

from PyQt5.QtCore import Qt, QPoint
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
    def __init__(self, QTWidget: QWidget, x: float, y: float, widgetType: str = "", hasReturnValue: bool = False, returnKey: str = None, configInfo=None, name: str = None):
        self.QTWidget = QTWidget
        self.setPosition(x, y)
        self.QTWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.QTWidget.customContextMenuRequested.connect(self.rightClickMenu)
        self.tabName = self.QTWidget.parent().objectName()

        if hasReturnValue and returnKey is None:
            print("No ReturnDataDict key specified for a widget.  This widget won't return data")
            self.hasReturnValue = False
        else:
            self.hasReturnValue = hasReturnValue

        if name is not None:
            self.QTWidget.setObjectName(name)

        self.returnKey = returnKey
        self.returnEvents = []

        self.x = x
        self.y = y
        self.type = widgetType
        self.xBuffer = 20
        self.yBuffer = 20
        self.width = 50
        self.height = 50
        self.draggable = True
        self.isDeleted = False

        # Generic parameters that many widgets might need
        self.borderWidth = 1
        self.font = "Arial"
        self.fontSize = 12
        self.hidden = False

        self.headerTextColor = "white"
        self.textColor = "white"
        self.borderColor = "black"
        self.red = 0
        self.green = 0
        self.blue = 0

        # More specific ones
        self.size = None  # For square widgets
        self.source = None
        self.transparent = None
        self.title = None

        if configInfo is not None:
            if Constants.BORDER_WIDTH_ATTRIBUTE in configInfo:
                self.borderWidth = int(configInfo[Constants.BORDER_WIDTH_ATTRIBUTE])
            if Constants.FONT_ATTRIBUTE in configInfo:
                self.font = configInfo[Constants.FONT_ATTRIBUTE]
            if Constants.FONT_SIZE_ATTRIBUTE in configInfo:
                self.fontSize = int(configInfo[Constants.FONT_SIZE_ATTRIBUTE])
            if Constants.BACKGROUND_ATTRIBUTE in configInfo:
                self.setColor(configInfo[Constants.BACKGROUND_ATTRIBUTE])
            if Constants.DRAGGABLE_ATTRIBUTE in configInfo:
                self.draggable = configInfo[Constants.DRAGGABLE_ATTRIBUTE]
            if Constants.TITLE_ATTRIBUTE in configInfo:
                self.title = configInfo[Constants.TITLE_ATTRIBUTE]
            if Constants.SIZE_ATTRIBUTE in configInfo:
                self.size = int(configInfo[Constants.SIZE_ATTRIBUTE])
            if Constants.SOURCE_ATTRIBUTE in configInfo:
                self.source = configInfo[Constants.SOURCE_ATTRIBUTE]
            if Constants.TRANSPARENT_ATTRIBUTE in configInfo:
                self.transparent = configInfo[Constants.TRANSPARENT_ATTRIBUTE]

        self.defaultFontSize = self.fontSize
        self.setFontInfo()

    def setSize(self, width, height):
        self.QTWidget.setMinimumWidth(width)
        self.QTWidget.setMaximumWidth(width)
        self.QTWidget.setMinimumHeight(height)
        self.QTWidget.setMaximumHeight(height)

        self.width = width
        self.height = height

    def rightClickMenu(self, e: QPoint):
        colorMenu = QMenu("Set color")
        whiteAction = colorMenu.addAction("White")
        blueAction = colorMenu.addAction("Blue")
        greyAction = colorMenu.addAction("Grey")
        defaultAction = colorMenu.addAction("Default")

        menu = QMenu()
        menu.addMenu(colorMenu)
        menu.addSeparator()
        increaseFontSizeAction = menu.addAction("Increase Font Size")
        decreaseFontSizeAction = menu.addAction("Decrease Font Size")
        defaultFontSizeAction = menu.addAction("Default Font Size")
        menu.addSeparator()
        if self.transparent is not None:
            menu.addAction("Toggle Transparency", self.toggleTransparency)
            menu.addSeparator()
        menu.addAction("Enable dragging", lambda draggable=True: self.setDraggable(draggable))
        menu.addAction("Disable dragging", lambda draggable=False: self.setDraggable(draggable))
        menu.addSeparator()
        menu.addAction("Delete", self.delete)
        menu.addSeparator()
        awesome = menu.addAction("Whack Patrick", lambda x=random.random() * 1500, y=random.random() * 1000: self.setPosition(x, y))  # This is silly

        action = menu.exec_(self.QTWidget.mapToGlobal(e))

        if action == whiteAction:
            self.setColor("white")
        if action == defaultAction:
            self.setColor("default")
        elif action == blueAction:
            self.setColor("blue")
        elif action == greyAction:
            self.setColor("grey")
        elif action == awesome:
            self.draggable = False
            print("Patrick has been whacked!!!!!!!!!!!!!!!!!!")
        elif action == increaseFontSizeAction:
            self.fontSize += 2
            self.setFontInfo()
        elif action == decreaseFontSizeAction:
            self.fontSize -= 2
            self.setFontInfo()
        elif action == defaultFontSizeAction:
            self.fontSize = self.defaultFontSize
            self.setFontInfo()

    def setColor(self, color, textColor=None, headerTextColor=None, borderColor=None):
        color = color.replace("Grey", "Gray")
        color = color.replace("grey", "gray")

        if color == "default":
            self.setDefaultAppearance()
        elif "rgb" in color:
            [red, green, blue] = [int(float(i)) for i in color.split("[")[1].split("]")[0].split(",")]  # Going to float then string fixes issues if the number is 0.0 or similar
            self.testTextColor(red, green, blue, textColor)
            self.testHeaderTextColor(headerTextColor)
            self.testBorderColor(borderColor)
            self.saveAndSetBackgroundColor(red, green, blue)
        elif convertNameToRGB(color):
            rgb = convertNameToRGB(color)
            self.testTextColor(rgb[0], rgb[1], rgb[2], textColor)
            self.testHeaderTextColor(headerTextColor)
            self.testBorderColor(borderColor)
            self.saveAndSetBackgroundColor(rgb[0], rgb[1], rgb[2])
        else:
            self.setDefaultAppearance()

    def saveAndSetBackgroundColor(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue
        self.setColorRGB(red, green, blue)

    def setColorRGB(self, red: int, green: int, blue: int):
        self.QTWidget.setStyleSheet("border: {3}px solid {5}; background: rgb({0}, {1}, {2}); color: {4}".format(red, green, blue, self.borderWidth, self.textColor, self.borderColor))

    def setDefaultAppearance(self):
        self.textColor = "black"
        self.headerTextColor = "black"
        self.QTWidget.setStyleSheet("color: black")

    def setFontInfo(self):
        self.QTWidget.setFont(QFont(self.font, self.fontSize))
        self.QTWidget.adjustSize()

    def testTextColor(self, red, green, blue, textColor=None):  # Checks text color against background r,g,b values, and makes it black or white depending on how bright the background is
        if textColor is not None:
            if "rgb[" in textColor:
                [red, green, blue] = textColor.split("[")[1].split("]")[0].split(",")
                self.textColor = "rgb({0},{1},{2})".format(red, green, blue)
            else:
                self.textColor = textColor
        elif max(red, green, blue) > 127:
            self.textColor = "black"
        else:
            self.textColor = "white"

    def testHeaderTextColor(self, textColor=None):
        if textColor is not None:
            if "rgb[" in textColor:
                [red, green, blue] = textColor.split("[")[1].split("]")[0].split(",")
                self.headerTextColor = "rgb({0},{1},{2})".format(red, green, blue)
            else:
                self.headerTextColor = textColor
        else:
            self.headerTextColor = self.textColor

    def testBorderColor(self, borderColor=None):
        if borderColor is not None:
            if "rgb[" in borderColor:
                [red, green, blue] = borderColor.split("[")[1].split("]")[0].split(",")
                self.borderColor = "rgb({0},{1},{2})".format(red, green, blue)
            else:
                self.borderColor = borderColor
        else:
            self.borderColor = "black"

    @staticmethod
    def getRGBFromColor(color):
        if "rgb[" in color:
            [red, green, blue] = color.split("[")[1].split("]")[0].split(",")
        elif "rgb(" in color:
            [red, green, blue] = color.split("(")[1].split(")")[0].split(",")
        else:
            [red, green, blue] = convertNameToRGB(color)

        return [red, green, blue]

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
        if self.isDeleted:
            self.QTWidget.setHidden(True)
        elif self.QTWidget.isHidden() != self.hidden:
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

    def getReturnEvents(self):
        temp = copy.deepcopy(self.returnEvents)
        self.returnEvents = []
        return temp

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

    def delete(self):
        self.setDeleted(True)

    def setDeleted(self, isDeleted):
        self.isDeleted = isDeleted

    def toggleTransparency(self):
        self.transparent = not self.transparent
        self.setColorRGB(self.red, self.green, self.blue)

    def getXMLStuff(self, item):
        """Default function to fill out the XML tag for an item.  DO NOT OVERWRITE UNLESS YOU KNOW WHAT YOU ARE DOING.  Calls customXMLStuff().  PUT YOUR CODE THERE INSTEAD"""

        if self.isDeleted:  # If the widget doesn't exist anymore, we don't save
            return

        tag = ElementTree.SubElement(item, Constants.WIDGET_NAME)
        tag.set(Constants.TYPE_ATTRIBUTE, str(self.type))
        tag.set(Constants.X_POS_ATTRIBUTE, str(self.x))
        tag.set(Constants.Y_POS_ATTRIBUTE, str(self.y))

        if self.title is not None:  # Ordered by importance
            tag.set(Constants.TITLE_ATTRIBUTE, self.title)
        if self.source is not None:
            tag.set(Constants.SOURCE_ATTRIBUTE, self.source)
        if self.size is not None:
            tag.set(Constants.SIZE_ATTRIBUTE, str(self.size))
        if self.transparent is not None:
            tag.set(Constants.TRANSPARENT_ATTRIBUTE, str(self.transparent))

        tag.set(Constants.HIDDEN_ATTRIBUTE, str(self.hidden))
        tag.set(Constants.DRAGGABLE_ATTRIBUTE, str(self.draggable))

        tag.set(Constants.FONT_ATTRIBUTE, str(self.font))
        tag.set(Constants.FONT_SIZE_ATTRIBUTE, str(self.fontSize))
        # tag.set(Constants.BORDER_WIDTH_ATTRIBUTE, str(self.borderWidth))

        self.customXMLStuff(tag)

    def customXMLStuff(self, tag):
        """Called during save operation.  Overwrite this method and put widget specific xml code here"""
        return tag
