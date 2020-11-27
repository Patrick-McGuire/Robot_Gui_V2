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
        GUICreator = GUIMaker("hi")
        GUICreator.CreateTab("1")
        GUICreator.CreateTab("2")
        GUICreator.start()

        #
        # tab1.layout = QVBoxLayout()
        # pushButton1 = QPushButton("PyQt5 button")
        # tab1.layout.addWidget(pushButton1)
        # tab1.setLayout(tab1.layout)


