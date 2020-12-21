import colorsys
import threading

import time
import copy

from GUIMaker import GUIMaker
from XmlParser import XmlParser

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFileDialog

from Constants import Constants


# This class handles the underlying functionality of updating widgets, running, and creating the GUI
def clamp(value, minValue, maxValue):
    """
    Clamps a value between the min and max value
    """
    return min(max(value, minValue), maxValue)


class CoreGUI(threading.Thread):
    """This class handles the underlying functionality of updating widgets, running, and creating the GUI"""

    CustomWidgetList = []

    def __init__(self, filePath):
        self.filePath = filePath

        self.GUIStarted = False
        self.GUIDone = False

        self.GUICreator = None
        self.mainWindow = None
        self.XMLParser = None

        self.activeClickedWidget = None
        self.activeOffset = [0, 0]

        self.dataPassDict = {}
        self.returnDict = {}
        self.rainbow = False
        self.hideOnClick = False
        self.hue = 0

        # Start the GUI
        threading.Thread.__init__(self)
        self.start()

        # Wait for the gui to actually start running
        while not self.GUIStarted:
            time.sleep(0.001)

    def run(self):
        self.GUICreator = GUIMaker()
        self.mainWindow = self.GUICreator.getMainWindow()

        # Create menu bar
        menuBar = self.mainWindow.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction("Open")  # Reload GUI from scratch??? OUCH!
        fileMenu.addAction("Save", self.saveGUI)  # Save to XML
        fileMenu.addAction("Save As", self.saveGUIAs)
        fileMenu.addSeparator()
        fileMenu.addAction("Quit", self.stop)

        # Menu bar for widgets
        widgetMenu = menuBar.addMenu("Widgets")
        colorSubMenu = widgetMenu.addMenu("Set Color")
        colorSubMenu.addAction("White", lambda color="white": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Blue", lambda color="blue": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Red", lambda color="rgb[255,0,0]": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Green", lambda color="rgb[0,100,0]": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Gray", lambda color="rgb[50,50,50]": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Default", lambda color="default": self.setColorOnALlWidgets(color))
        colorSubMenu.addSeparator()
        colorSubMenu.addAction("Toggle Rainbow", self.toggleRainbow)
        widgetMenu.addSeparator()
        widgetMenu.addAction("Lock all widgets", lambda draggable=False: self.setDraggingOnALlWidgets(draggable))
        widgetMenu.addAction("Unlock all widgets", lambda draggable=True: self.setDraggingOnALlWidgets(draggable))
        widgetMenu.addAction("Disable hide on click", lambda enabled=False: self.setHideOnClick(enabled))
        widgetMenu.addAction("Enable hide on click", lambda enabled=True: self.setHideOnClick(enabled))
        widgetMenu.addAction("Show all widgets", self.showAllWidgets)

        # Menu bar for themes
        themeMenu = menuBar.addMenu("Theme")
        themeMenu.addAction("Light", lambda theme="light": self.setTheme(theme))
        themeMenu.addAction("Dark", lambda theme="dark": self.setTheme(theme))
        themeMenu.addAction("Blue", lambda theme="blue": self.setTheme(theme))
        themeMenu.addSection("Experimental")
        themeMenu.addAction("Red", lambda theme="rgb[100,0,0]": self.setTheme(theme))
        themeMenu.addAction("Black", lambda theme="rgb[0,0,0]": self.setTheme(theme))

        helpMenu = menuBar.addMenu("Help")
        helpMenu.addAction("Whack Patrick", self.toggleRainbow)

        # PlaceHolders
        self.GUICreator.createTab("Settings")
        self.GUICreator.createTextBoxDropDownWidget("Settings", 100, 100)
        self.GUICreator.createButton("Settings", "Whack Patrick", 100, 300)
        self.GUICreator.createSimpleDropDown("Settings", 400, 100)

        self.XMLParser = XmlParser(self.filePath, self.GUICreator)
        returnData = self.XMLParser.getConfigData()

        self.setTheme(returnData[Constants.THEME_ATTRIBUTE])

        self.setupEventHandler()

        # QTimer to run the update method
        timer = QTimer()
        timer.timeout.connect(self.updateGUI)
        timer.start(10)

        # Start GUI thread
        self.GUIStarted = True
        self.GUICreator.start()
        self.GUIDone = True

    def stop(self):
        self.GUICreator.stop()

    def updateDataPassDict(self, dataPassDict):
        self.dataPassDict = dataPassDict

    def getReturnDict(self):
        return self.returnDict

    def setTheme(self, theme: str):
        """Function to set a theme for the whole GUI"""

        if theme == "dark":
            self.setColorOnALlWidgets("grey")
            self.GUICreator.setGUIColor(30, 30, 30)
        elif theme == "light":
            self.setColorOnALlWidgets("default")
            self.GUICreator.setGUIColor(250, 250, 250)
        elif theme == "blue":
            self.setColorOnALlWidgets("rgb[0,0,50]")
            self.GUICreator.setGUIColor(0, 0, 40)
        elif "rgb" in theme:
            self.setColorOnALlWidgets(theme)
            [red, green, blue] = theme.split("[")[1].split("]")[0].split(",")
            self.GUICreator.setGUIColor(int(float(red)), int(float(green)), int(float(blue)))

    def updateGUI(self):
        listOfWidgets = self.GUICreator.GetWidgetList()
        returnDict = {}

        for widget in listOfWidgets:
            widget.update(self.dataPassDict)

            if widget.returnsData():
                returnDict[widget.getReturnKey()] = widget.getData()

        self.returnDict = copy.deepcopy(returnDict)

        if self.rainbow:
            self.hue += 0.01
            if self.hue > 1:
                self.hue = 0

            [red, green, blue] = colorsys.hsv_to_rgb(self.hue, 1, 1)
            self.setColorOnALlWidgets("rgb[{0},{1},{2}]".format(red * 255, green * 255, blue * 255))

    def setupEventHandler(self):
        """Overwrites mainWindow's event handlers to ones in this class"""
        self.mainWindow.mouseMoveEvent = self.mouseMoveEvent
        self.mainWindow.mouseReleaseEvent = self.mouseReleaseEvent
        self.mainWindow.mousePressEvent = self.mousePressEvent

    def mouseMoveEvent(self, e):
        """Moves the active widget to the position of the mouse if we are currently clicked"""
        if self.activeClickedWidget is not None and self.activeClickedWidget.isDraggable():
            x = clamp(e.x() - self.activeOffset[0], 0, float(self.mainWindow.width()) - 30)
            y = clamp(e.y() - self.activeOffset[1], 0, float(self.mainWindow.height()) - 50)
            self.activeClickedWidget.setPosition(x, y)

    def mousePressEvent(self, e: QMouseEvent):
        """Determines if we clicked on a widget"""
        currentTabIndex = self.mainWindow.centralWidget().currentIndex()
        tabList = self.GUICreator.getTabNames()

        if self.activeClickedWidget is None and e.button() == 1:
            listOfWidgets = self.GUICreator.GetWidgetList()
            for widget in reversed(listOfWidgets):
                if widget.isPointInWidget(float(e.x()), float(e.y())) and tabList[currentTabIndex] == widget.getTabName():
                    if self.hideOnClick:
                        widget.hide()
                    else:
                        self.activeClickedWidget = widget
                        self.activeOffset = [float(e.x()) - widget.x, float(e.y()) - widget.y]
                    return

    def mouseReleaseEvent(self, e):
        if self.activeClickedWidget is not None:
            self.activeClickedWidget = None

    def setColorOnALlWidgets(self, color):
        """Sets colors on all widgets"""
        listOfWidgets = self.GUICreator.GetWidgetList()

        for widget in listOfWidgets:
            widget.setColor(color)

    def setDraggingOnALlWidgets(self, draggable):
        """Sets colors on all widgets"""
        listOfWidgets = self.GUICreator.GetWidgetList()

        for widget in listOfWidgets:
            widget.setDraggable(draggable)

    def toggleRainbow(self):
        self.rainbow = not self.rainbow

    def setHideOnClick(self, enabled: bool):
        self.hideOnClick = enabled

    def showAllWidgets(self):
        """Shows all widgets"""
        listOfWidgets = self.GUICreator.GetWidgetList()

        for widget in listOfWidgets:
            widget.show()

    def saveGUI(self, fileName=None):
        """Generates output XML, and writes that to a file"""
        if fileName is None:
            fileName = self.filePath

        print(fileName)
        # TODO: add xml output function here

    def saveGUIAs(self):
        """Opens a file dialog, then calls the save function with the full filename"""
        name = QFileDialog.getSaveFileName(self.mainWindow, 'Save File')
        self.saveGUI(name[0])
