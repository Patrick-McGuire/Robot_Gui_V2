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

        # Start the GUI
        threading.Thread.__init__(self)
        self.start()

        # Wait for the gui to actually start running
        while not self.GUIStarted:
            time.sleep(0.001)

    def run(self):
        self.GUICreator = GUIMaker()
        self.GUICreator.SetTitle("Pr0b0t__c0nTr0l")
        self.GUICreator.CreateTab("1")
        self.GUICreator.CreateTab("2")

        self.GUICreator.CreateVideoWidget("1", 0, 0, 1500, 1000)

        self.GUICreator.CreateButton("1", "test", 100, 200)
        self.GUICreator.CreateButton("1", "2", 100, 250)
        self.GUICreator.CreateButton("1", "3", 100, 300)

        self.GUICreator.CreateTextBox("1", 1200, 200)
        self.GUICreator.CreateTextBox("1", 1200, 300)
        self.GUICreator.CreateTextBox("1", 1200, 400)

        self.GUICreator.CreateCompassWidget("1", 100, 100, 200)
        self.GUICreator.CreateCompassWidget("1", 100, 100, 150)

        self.GUICreator.CreateSimpleDropDown("2", 100, 100)

        self.mainWindow = self.GUICreator.getMainWindow()
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
