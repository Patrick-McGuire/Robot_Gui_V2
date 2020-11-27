import time

from CoreGUI import CoreGUI


class RobotGUI2:
    def __init__(self, filePath):
        self.coreGui = CoreGUI(filePath)

        while not self.coreGui.GUIDone:
            self.coreGui.updateGUI()
            time.sleep(0.01)

        self.coreGui.stop()
