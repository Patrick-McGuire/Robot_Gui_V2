"""
Function calls to actually create GUI elements
"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget

from WidgetClasses import SimpleButton
from WidgetClasses import TextBoxWidget
from WidgetClasses import SimpleDropDown


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
        
    def getMainWindow(self):
        return self.mainWindow
