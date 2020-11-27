import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout

from GUIMaker import GUIMaker


# This class handles the underlying functionality of updating widgets, running, and creating the GUI
class CoreGUI(threading.Thread):
    def __init__(self, filePath):
        self.filePath = filePath
        self.application = None
        self.mainWindow = None

        # Start the GUI
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        GUICreator = GUIMaker("PRoBoT_ConTrOl")
        GUICreator.CreateTab("1")
        GUICreator.CreateTab("2")

        GUICreator.CreateButton("1", "test", 0, 10)
        GUICreator.CreateButton("1", "2", 100, 100)
        GUICreator.CreateButton("1", "3", 100, 0)

        # GUICreator.CreateTextBox("1")

        GUICreator.start()
