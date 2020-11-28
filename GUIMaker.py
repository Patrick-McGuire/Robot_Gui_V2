"""
Function calls to actually create GUI elements
"""
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QMenuBar

from WidgetClasses import SimpleButton
from WidgetClasses import TextBoxWidget
from WidgetClasses import SimpleDropDown
from WidgetClasses import VideoWidget
from WidgetClasses.CompassWidget import CompassWidget


class GUIMaker(object):
    tabs = {}
    widgetList = []

    def __init__(self):
        self.application = QApplication([])
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(0, 0, 1500, 1000)
        self.tabHolderWidget = QTabWidget()
        self.tabHolderWidget.resize(300, 200)

        # menubar = QMenuBar()
        # layout.addWidget(menubar, 0, 0)
        # actionFile = menubar.addMenu("File")
        # actionFile.addAction("New")
        # actionFile.addAction("Open")
        # actionFile.addAction("Save")
        # actionFile.addSeparator()
        # actionFile.addAction("Quit")
        # menubar.addMenu("Edit")
        # menubar.addMenu("View")
        # menubar.addMenu("Help")

    def start(self):
        self.mainWindow.setCentralWidget(self.tabHolderWidget)

        self.mainWindow.show()
        self.application.exec_()

    def stop(self):
        self.application.exit()

    def SetTitle(self, title):
        self.mainWindow.setWindowTitle(title)

    def GetWidgetList(self):
        return self.widgetList

    def CreateTab(self, name):
        """Creates a tab with the specified name"""
        self.tabs[name] = QWidget()

        self.tabHolderWidget.addTab(self.tabs[name], name)

    def CreateButton(self, tabName, text, x, y):
        """Creates a basic button widget in the tab name specified"""
        self.widgetList.append(SimpleButton.SimpleButton(self.tabs[tabName], text, x, y))

    def CreateTextBox(self, tabName, x, y):
        """Creates a text box widget in the tab name specified"""
        self.widgetList.append(TextBoxWidget.TextBoxWidget(self.tabs[tabName], x, y))

    def CreateSimpleDropDown(self, tabName, x, y):
        """Creates a text box widget in the tab name specified"""
        self.widgetList.append(SimpleDropDown.SimpleDropDown(self.tabs[tabName], x, y))

    def CreateVideoWidget(self, tabName, x, y, width, height):
        """Creates a video widget in the tab name specified"""
        self.widgetList.append(VideoWidget.VideoWidget(self.tabs[tabName], x, y, width, height))

    def CreateCompassWidget(self, tabName, x, y, size):
        self.widgetList.append(CompassWidget(self.tabs[tabName], x, y, size))

    def getMainWindow(self):
        return self.mainWindow
