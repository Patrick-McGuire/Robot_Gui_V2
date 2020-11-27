# from PyQt5.QtWidgets import QApplication, QLabel, QFrame, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout

import threading

class RobotGUI(threading.Thread):
    def __init__(self):
        self.appWindow = None

        # Start the thread
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.appWindow = QApplication([])
        app = QMainWindow()
        app.setGeometry(0, 0, 500, 500)
        app.setWindowTitle("Hi")

        tabHolderWidget = QTabWidget()
        tab1 = QTabWidget()
        tab11 = QWidget()
        tab22 = QWidget()
        tab1.addTab(tab11, "Tab 1")
        tab1.addTab(tab22, "Tab 2")

        tab2 = QWidget()
        tabHolderWidget.resize(300, 200)
        tabHolderWidget.addTab(tab1, "Tab 1")
        tabHolderWidget.addTab(tab2, "Tab 2")

        tab11.layout = QVBoxLayout()
        pushButton1 = QPushButton("PyQt5 button")
        tab11.layout.addWidget(pushButton1)
        tab11.setLayout(tab11.layout)

        app.setCentralWidget(tabHolderWidget)
        app.show()


        self.appWindow.exec_()

a = RobotGUI()
while True:
    pass

