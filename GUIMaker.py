"""
Function calls to actually create GUI elements
"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton

from WidgetClasses import SimpleButton
from WidgetClasses import TextBoxWidget


class GUIMaker(object):
    tabs = {}

    widgetList = []

    def __init__(self):
        self.application = QApplication([])
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(0, 0, 500, 500)

        self.tabHolderWidget = QTabWidget()
        self.tabHolderWidget.resize(300, 200)

    def start(self):
        self.mainWindow.setCentralWidget(self.tabHolderWidget)

        self.mainWindow.show()
        self.application.exec_()

    def SetTitle(self, title):
        self.mainWindow.setWindowTitle(title)

    def GetWidgetList(self):
        return self.widgetList

    def CreateTab(self, name):
        self.tabs[name] = QWidget()

        self.tabHolderWidget.addTab(self.tabs[name], name)

    def CreateButton(self, tabName, text, x, y):
        self.widgetList.append(SimpleButton.SimpleButton(self.tabs[tabName], text, x, y))

    def CreateTextBox(self, tabName, x, y):
        self.widgetList.append(TextBoxWidget.TextBoxWidget(self.tabs[tabName], x, y))
