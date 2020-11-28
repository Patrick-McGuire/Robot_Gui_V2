"""
Function calls to actually create GUI elements
"""
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QMenuBar

from WidgetClasses import SimpleButton
from WidgetClasses import TextBoxWidget
from WidgetClasses import SimpleDropDown
from WidgetClasses import VideoWidget
from WidgetClasses import TextBoxDropDownWidget


class GUIMaker(object):
    tabs = {}
    widgetList = []

    def __init__(self):
        self.application = QApplication([])
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(0, 0, 1500, 1000)
        self.tabHolderWidget = QTabWidget()
        self.tabHolderWidget.resize(300, 200)

        menuBar = self.mainWindow.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction("New")
        fileMenu.addAction("Open")
        fileMenu.addAction("Save")
        fileMenu.addSeparator()
        fileMenu.addAction("Quit")

        menuBar.addMenu("Edit")
        menuBar.addMenu("View")
        helpMenu = menuBar.addMenu("Help")
        helpMenu.addAction("Whack Patrick")

        self.widgetsCreated = 0

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

    def CreateTextBoxDropDownWidget(self, tabName, x, y):
        """Creates a textbox with a drop down in the tab name specified"""
        self.widgetList.append(TextBoxDropDownWidget.TextBoxDropDownWidget(self.tabs[tabName], "textBoxDropDown_{}".format(self.widgetsCreated), x, y))
        self.widgetsCreated = self.widgetsCreated + 1

    def getMainWindow(self):
        return self.mainWindow
