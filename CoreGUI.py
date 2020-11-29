import colorsys
import threading

import time
import copy

from GUIMaker import GUIMaker

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QMouseEvent


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

        self.activeClickedWidget = None
        self.activeOffset = [0, 0]

        self.dataPassDict = {}
        self.returnDict = {}
        self.rainbow = False
        self.hue = 0

        # Start the GUI
        threading.Thread.__init__(self)
        self.start()

        # Wait for the gui to actually start running
        while not self.GUIStarted:
            time.sleep(0.001)

    def run(self):
        self.GUICreator = GUIMaker()
        self.GUICreator.SetTitle("Pr0b0t__c0nTr0l")
        self.mainWindow = self.GUICreator.getMainWindow()

        menuBar = self.mainWindow.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction("New")
        fileMenu.addAction("Open")
        fileMenu.addAction("Save")
        fileMenu.addSeparator()
        fileMenu.addAction("Quit")

        widgetMenu = menuBar.addMenu("Widgets")
        colorSubMenu = widgetMenu.addMenu("Set Color")
        colorSubMenu.addAction("White", lambda color="white": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Blue", lambda color="blue": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Red", lambda color="rgb[255,0,0]": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Green", lambda color="rgb[0,100,0]": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Gray", lambda color="rgb[50,50,50]": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Default", lambda color="default": self.setColorOnALlWidgets(color))
        colorSubMenu.addAction("Toggle Rainbow", self.toggleRainbow)

        helpMenu = menuBar.addMenu("Help")
        helpMenu.addAction("Whack Patrick")

        self.GUICreator.CreateTab("1")
        self.GUICreator.CreateTab("2")

        self.GUICreator.CreateVideoWidget("1", 0, 0, 1500, 1000)

        self.GUICreator.CreateButton("1", "test", 100, 200)
        self.GUICreator.CreateButton("1", "2", 100, 250)
        self.GUICreator.CreateButton("1", "3", 100, 300)

        self.GUICreator.CreateTextBox("1", 1200, 200)
        self.GUICreator.CreateTextBox("1", 1200, 300)
        self.GUICreator.CreateTextBox("1", 1200, 400)

        self.GUICreator.CreateCompassWidget("1", 250, 150, 200)
        self.GUICreator.CreateCompassWidget("1", 1200, 700, 150)

        self.GUICreator.CreateSimpleDropDown("2", 100, 100)

        self.GUICreator.CreateTextBoxDropDownWidget("1", 100, 400)
        self.GUICreator.CreateTextBoxDropDownWidget("1", 100, 550)
        self.GUICreator.CreateTextBoxDropDownWidget("1", 1200, 500)

        self.setupEventHandler()

        # QTimer to run the update method
        timer = QTimer()
        timer.timeout.connect(self.updateGUI)
        timer.start(10)

        self.GUIStarted = True
        self.GUICreator.start()

        self.GUIDone = True

    def stop(self):
        self.GUICreator.stop()

    def updateDataPassDict(self, dataPassDict):
        self.dataPassDict = dataPassDict

    def getReturnDict(self):
        return self.returnDict

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
        if self.activeClickedWidget is not None:
            x = clamp(e.x() - self.activeOffset[0], 0, float(self.mainWindow.width()) - 30)
            y = clamp(e.y() - self.activeOffset[1], 0, float(self.mainWindow.height()) - 50)
            self.activeClickedWidget.setPosition(x, y)

    def mousePressEvent(self, e: QMouseEvent):
        """Determines if we clicked on a widget"""
        if self.activeClickedWidget is None and e.button() == 1:
            listOfWidgets = self.GUICreator.GetWidgetList()
            for widget in reversed(listOfWidgets):
                if widget.isPointInWidget(float(e.x()), float(e.y())):
                    self.activeClickedWidget = widget
                    self.activeOffset = [float(e.x()) - widget.x, float(e.y()) - widget.y]
                    return

    def mouseReleaseEvent(self, e):
        if self.activeClickedWidget is not None:
            # self.activeClickedWidget.setPosition(self.x, self.y)
            self.activeClickedWidget = None

    def setColorOnALlWidgets(self, color):
        """Sets colors on all widgets"""
        listOfWidgets = self.GUICreator.GetWidgetList()

        for widget in listOfWidgets:
            widget.setColor(color)

    def toggleRainbow(self):
        self.rainbow = not self.rainbow
