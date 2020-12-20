

from CoreGUI import CoreGUI


class RobotGUI2:
    dataPassDict = {}

    def __init__(self, filePath):
        self.coreGui = CoreGUI(filePath)

    def updateInfo(self, dataPassDict):
        self.coreGui.updateDataPassDict(dataPassDict)

    def getDataPassDict(self):
        return self.dataPassDict

    def stop(self):
        self.coreGui.stop()

    def isDone(self):
        return self.coreGui.GUIDone
