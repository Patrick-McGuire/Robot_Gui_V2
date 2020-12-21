import time
import random
import cv2

from RobotGUI2 import RobotGUI2

# GUI = RobotGUI2("config/GUIConfig.xml")
GUI = RobotGUI2("config/BasicConfig.xml", testMode=True)

cap = cv2.VideoCapture(0)

while not GUI.isDone():
    ret, frame = cap.read()

    dataPassDict = {"test": "{}".format(random.random()), "webcam": frame, "batteryVoltage": "{}".format(random.random())}

    testDict = {"aaa": [["hi", "aaa"], ["bbb", random.random()]], "bbb": [["aa", "  {}".format(random.random())], ["bbb", random.random()], ["c", random.random()], ["ddddddddd", random.random()]]}
    dataPassDict["diagnostics_agg"] = testDict

    annunciator = [["Overall", 0, "Test"], ["Battery", 1, "Test2"], ["Lights", 2, "Test3"], ["aaaaaaaaaaaaaaaaaaaaaaaaaa", 0, "test4"]]
    dataPassDict["annunciator"] = annunciator

    annunciator2 = [["aaa", 2, "Test"], ["bbb", 0, "Test2"], ["ccc", 0, "Test3"], ["ddddd", 0, "test4"]]
    dataPassDict["annunciator_2"] = annunciator2

    GUI.updateInfo(dataPassDict)

    # print(self.coreGui.getReturnDict())
    time.sleep(0.01)

GUI.stop()
