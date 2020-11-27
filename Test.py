from PyQt5.QtWidgets import QApplication, QLabel
import threading


class RobotGUI(threading.Thread):
    def __init__(self, filePath):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        # Init the window