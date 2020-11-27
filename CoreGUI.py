import threading
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout


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
        self.application = QApplication([])
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(0, 0, 500, 500)

        self.mainWindow.setWindowTitle("Hi")

        tabHolderWidget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tabHolderWidget.resize(300, 200)
        tabHolderWidget.addTab(tab1, "Tab 1")
        tabHolderWidget.addTab(tab2, "Tab 2")

        tab1.layout = QVBoxLayout()
        pushButton1 = QPushButton("PyQt5 button")
        tab1.layout.addWidget(pushButton1)
        tab1.setLayout(tab1.layout)

        self.mainWindow.setCentralWidget(tabHolderWidget)


        self.mainWindow.show()
        self.application.exec_()


