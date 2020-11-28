import time
import random
import cv2

from CoreGUI import CoreGUI


class RobotGUI2:
    def __init__(self, filePath):
        cap = cv2.VideoCapture(0)
        self.coreGui = CoreGUI(filePath)

        while not self.coreGui.GUIDone:
            ret, frame = cap.read()

            dataPassDict = {"test": "{}".format(random.random()), "test1": "{}".format(time.time()), "image": frame}
            self.coreGui.updateDataPassDict(dataPassDict)

            # print(self.coreGui.getReturnDict())
            time.sleep(0.01)

        self.coreGui.stop()
