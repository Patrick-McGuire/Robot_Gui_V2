import threading

import time
import random

from GUIMaker import GUIMaker


# This class handles the underlying functionality of updating widgets, running, and creating the GUI
class CoreGUI(threading.Thread):
    CustomWidgetList = []

    def __init__(self, filePath):
        self.filePath = filePath

        self.GUIDone = False

        self.GUICreator = None

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

        self.GUICreator.CreateTextBox("1", 130, 130)

        self.GUICreator.CreateSimpleDropDown("2", 100, 100)

        self.GUICreator.start()

        self.GUIDone = True

    def stop(self):
        self.GUICreator.stop()

    def updateGUI(self):
        listOfWidgets = self.GUICreator.GetWidgetList()

        self.GUICreator.SetTitle(str(time.time()))

        dataPassDict = {"test": "{}".format(random.random()), "test1": "{}".format(time.time())}

        for widget in listOfWidgets:
            widget.update(dataPassDict)
