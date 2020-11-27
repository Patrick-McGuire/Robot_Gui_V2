import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout

import time

from GUIMaker import GUIMaker


# This class handles the underlying functionality of updating widgets, running, and creating the GUI
class CoreGUI(threading.Thread):
    CustomWidgetList = []

    def __init__(self, filePath):
        self.filePath = filePath

        self.GUIDone = False

        self.GUICreator = None
        self.mainWindow = None

        self.activeClickedWidget = None
        self.activeOffset = [0, 0]

        # Start the GUI
        threading.Thread.__init__(self)
        self.start()

        time.sleep(0.5)

    def run(self):
        self.GUICreator = GUIMaker()
        self.GUICreator.CreateTab("1")
        self.GUICreator.CreateTab("2")

        self.GUICreator.CreateButton("1", "test", 0, 10)
        self.GUICreator.CreateButton("1", "2", 100, 100)
        self.GUICreator.CreateButton("1", "3", 100, 0)

        self.GUICreator.CreateTextBox("1", 130, 120)

        self.mainWindow = self.GUICreator.getMainWindow()
        self.setupEventHandler()

        self.GUICreator.start()

        self.GUIDone = True

    def stop(self):
        self.GUICreator.stop()

    def updateGUI(self):
        listOfWidgets = self.GUICreator.GetWidgetList()

        self.GUICreator.SetTitle(str(time.time()))

        dataPassDict = {"test": 0, "test1": "aaaaaaaaaa"}

        for widget in listOfWidgets:
            widget.update(dataPassDict)

    # Overwrites mainWindow's event handlers to ones in this class
    def setupEventHandler(self):
        self.mainWindow.mouseMoveEvent = self.mouseMoveEvent
        self.mainWindow.mouseReleaseEvent = self.mouseReleaseEvent
        self.mainWindow.mousePressEvent = self.mousePressEvent

    def mouseMoveEvent(self, e):
        """Moves the active widget to the position of the mouse if we are currently clicked"""
        # print(self.activeClickedWidget)
        if self.activeClickedWidget is not None:
            self.activeClickedWidget.setPosition(e.x() - self.activeOffset[0], e.y() - self.activeOffset[1])

    def mousePressEvent(self, e):
        """Determines if we clicked on a widget"""
        if self.activeClickedWidget is None:
            listOfWidgets = self.GUICreator.GetWidgetList()
            for widget in listOfWidgets:
                if widget.isPointInWidget(float(e.x()), float(e.y())):
                    self.activeClickedWidget = widget
                    self.activeOffset = [float(e.x()) - widget.x, float(e.y()) - widget.y]
                    return

    def mouseReleaseEvent(self, e):
        self.activeClickedWidget = None
