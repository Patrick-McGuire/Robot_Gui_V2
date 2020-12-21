

from CoreGUI import CoreGUI


class RobotGUI2:
    dataPassDict = {}

    def __init__(self, filePath, testMode=False):
        self.coreGui = CoreGUI(filePath, createSettings=testMode)

    def updateInfo(self, dataPassDict):
        self.coreGui.updateDataPassDict(dataPassDict)

    def getDataPassDict(self):
        """Doesn't really do anything yet"""
        return self.dataPassDict

    def stop(self):
        self.coreGui.stop()

    def isDone(self):
        return self.coreGui.GUIDone
