from CoreGUI import CoreGUI


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
