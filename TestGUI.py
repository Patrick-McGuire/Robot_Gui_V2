import time
import random
import cv2

from RobotGUI2 import RobotGUI2

# GUI = RobotGUI2("config/GUIConfig.xml")
GUI = RobotGUI2("config/BasicConfig.xml")

cap = cv2.VideoCapture(0)

while not GUI.isDone():
    ret, frame = cap.read()

    dataPassDict = {"test": "{}".format(random.random()), "webcam": frame, "batteryVoltage": "{}".format(random.random())}
    GUI.updateInfo(dataPassDict)

    # print(self.coreGui.getReturnDict())
    time.sleep(0.01)

GUI.stop()
