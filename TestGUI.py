import time
import random
import cv2
import math
import random

from RobotGUI2 import RobotGUI2


def callback(data):
    """You can pass callbacks to the GUI now, that can be triggered from buttons"""
    print(data)


if __name__ == '__main__':
    # GUI = RobotGUI2("config/GUIConfig.xml")
    GUI = RobotGUI2("config/BasicConfig.xml", testMode=True)

    GUI.addCallback(callback, "button1")
    GUI.addCallback(callback, "complete_console_test")

    video = True
    cap = cv2.VideoCapture(0)
    cap.setExceptionMode(True)
    if not cap.isOpened():
        video = False

    i = 0
    j = 0

    while not GUI.isDone():
        GUI.processCallbacks()

        i += 3
        if i > 360:
            i = 0

        j += 0.5
        if j > 360:
            j = 0

        dataPassDict = {"test": "{}".format(random.random()), "batteryVoltage": "{}".format(random.random()),
                        "current": str(random.random() * 100), "spinny": i}

        if video:
            try:
                ret, frame = cap.read()
                dataPassDict["webcam"] = frame
            except cv2.error:
                video = False
                print("Can't get video frame")

        dataPassDict["roll"] = i
        dataPassDict["pitch"] = 10
        dataPassDict["yaw"] = i
        dataPassDict["altitude"] = float(i) / 80.0 - 10
        dataPassDict["groundSpeed"] = 19.5
        dataPassDict["verticalSpeed"] = (i / 15) - 10
        dataPassDict["terrainAlt"] = (-i / 5) + 40
        dataPassDict["j"] = j
        dataPassDict["slowSweep"] = 1 - float(j) / 180.0

        dataPassDict["status"] = int((float(i) / 360.0) * 3)

        r = random.random() * 0.1 + 0.95
        dataPassDict["x_position_global"] = math.cos(math.radians(j)) * r
        dataPassDict["y_position_global"] = math.sin(math.radians(j)) * r

        if i < 100:
            dataPassDict["allowedToArm"] = False
        else:
            dataPassDict["allowedToArm"] = True

        if i < 200:
            dataPassDict["armed"] = False
        else:
            dataPassDict["armed"] = True

        testDict = {"aaa": [["hi", "aaa"], ["bbb", random.random()]],
                    "bbb": [["aa", "  {}".format(random.random())], ["bbb", random.random()], ["c", random.random()],
                            ["ddddddddd", random.random()]]}
        dataPassDict["diagnostics_agg"] = testDict

        annunciator = [["Overall", 0, "Test"], ["Battery", 1, "Test2"], ["Lights", 2, "Test3"],
                       ["aaaaaaaaaaaaaaaaaaaaaaaaaa", 0, "test4"]]
        dataPassDict["annunciator"] = annunciator

        annunciator2 = [["aaa", 2, "Test"], ["bbb", 0, "Test2"], ["ccc", 0, "Test3"], ["ddddd", 3, "test4"]]
        dataPassDict["annunciator_2"] = annunciator2

        statusEvent = [["help", 1], ["aaaaaaaaaaaaaaaa", 2], ["bbbbbbbbbbb", 3], ["qqqqqqqqq", 0]]
        dataPassDict["status_event"] = statusEvent

        GUI.updateInfo(dataPassDict)

        GUI.updateConsole("testarray", str(random.random()))
        GUI.updateConsole("complete_console_test", str(random.random()))

        # print(self.coreGui.getReturnDict())
        time.sleep(0.01)

    GUI.stop()
