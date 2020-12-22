from CoreGUI import CoreGUI


class RobotGUI2:
    dataPassDict = {}

    def __init__(self, filePath, testMode=False, loadXMLFirst=True):
        self.coreGui = CoreGUI(filePath, createSettings=testMode, loadXMLFirst=loadXMLFirst)

    def updateInfo(self, dataPassDict):
        self.coreGui.updateDataPassDict(dataPassDict)

    def updateConsole(self, console, value):
        self.coreGui.updateConsole(console, value)

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
