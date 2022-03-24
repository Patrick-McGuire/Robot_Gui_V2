import sys
import os

from CoreGUI import CoreGUI

if sys.platform == "linux":  # I don't even know anymore
    if "QT_QPA_PLATFORM_PLUGIN_PATH" in os.environ:
        os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")  # https://stackoverflow.com/questions/63829991/qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-though-it


class RobotGUI2:
    dataPassDict = {}
    callbacks = {}

    def __init__(self, filePath, testMode=False, loadXMLFirst=True):
        self.coreGui = CoreGUI(filePath, createSettings=testMode, loadXMLFirst=loadXMLFirst)

    def updateInfo(self, dataPassDict):
        self.coreGui.updateDataPassDict(dataPassDict)

    def updateConsole(self, console, value):
        self.coreGui.updateConsole(console, value)

    def processCallbacks(self):
        callbackQueue = self.coreGui.getCallbackQueue()
        self.coreGui.clearCallbackQueue()

        for callback in callbackQueue:
            if callback[0] in self.callbacks:
                self.callbacks[callback[0]](callback[1])  # What amazingly clean code
            else:
                print("That isn't a valid callback")

    def addCallback(self, callback, target):
        self.callbacks[target] = callback

    def loadXML(self, filePath=None):
        if filePath is not None:
            self.coreGui.filePath = filePath
            self.coreGui.needsToLoadXML = True

    def getDataPassDict(self):
        """Doesn't really do anything yet"""
        return self.dataPassDict

    def stop(self):
        self.coreGui.stop()

    def isDone(self):
        return self.coreGui.GUIDone
