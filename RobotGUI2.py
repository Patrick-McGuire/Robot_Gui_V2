import time
import random

from CoreGUI import CoreGUI


class RobotGUI2:
    def __init__(self, filePath):
        self.coreGui = CoreGUI(filePath)

        while not self.coreGui.GUIDone:
            dataPassDict = {"test": "{}".format(random.random()), "test1": "{}".format(time.time())}
            self.coreGui.updateDataPassDict(dataPassDict)

            #print(self.coreGui.getReturnDict())
            time.sleep(0.01)

        self.coreGui.stop()
