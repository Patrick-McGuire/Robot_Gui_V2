"""
Function calls to actually create GUI elements
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout


class GUIMaker(object):
    tabs = {}

    def __init__(self, title):
        self.application = QApplication([])
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(0, 0, 500, 500)

        self.SetTitle(title)

        self.tabHolderWidget = QTabWidget()
        self.tabHolderWidget.resize(300, 200)

    def start(self):
        self.mainWindow.setCentralWidget(self.tabHolderWidget)

        self.mainWindow.show()
        self.application.exec_()

    def SetTitle(self, title):
        self.mainWindow.setWindowTitle("title")

    def CreateTab(self, name):
        self.tabs[name] = QWidget()

        self.tabHolderWidget.addTab(self.tabs[name], name)

    def CreateTextBox(self):
        pass
