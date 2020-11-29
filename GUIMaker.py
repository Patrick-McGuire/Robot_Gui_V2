"""
Function calls to actually create GUI elements
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget

from WidgetClasses import SimpleButton
from WidgetClasses import TextBoxWidget
from WidgetClasses import SimpleDropDown
from WidgetClasses import VideoWidget
from WidgetClasses.CompassWidget import CompassWidget
from WidgetClasses import TextBoxDropDownWidget


class GUIMaker(object):
    tabs = {}
    tabNames = []
    widgetList = []

    def __init__(self):
        self.application = QApplication([])
        self.mainWindow = QMainWindow()

        self.tabHolderWidget = QTabWidget()
        self.tabHolderWidget.resize(300, 200)

        self.widgetsCreated = 0

    def start(self):
        self.mainWindow.setCentralWidget(self.tabHolderWidget)

        self.mainWindow.show()
        self.application.exec_()

    def stop(self):
        self.application.exit()

    def SetTitle(self, title):
        self.mainWindow.setWindowTitle(title)

    def setWindowGeometry(self, width, height):
        self.mainWindow.setGeometry(0, 0, int(width), int(height))

    def GetWidgetList(self):
        return self.widgetList

    def createTab(self, name):
        """Creates a tab with the specified name"""
        self.tabs[name] = QWidget()
        self.tabs[name].setObjectName(name)

        self.tabHolderWidget.addTab(self.tabs[name], name)
        self.tabNames.append(name)

    def createButton(self, tabName, text, x, y):
        """Creates a basic button widget in the tab name specified"""
        self.widgetList.append(SimpleButton.SimpleButton(self.tabs[tabName], text, x, y))

    def createTextBox(self, tabName, x, y, widgetInfo):
        """Creates a text box widget in the tab name specified"""
        self.widgetList.append(TextBoxWidget.TextBoxWidget(self.tabs[tabName], x, y, widgetInfo))

    def createSimpleDropDown(self, tabName, x, y):
        """Creates a text box widget in the tab name specified"""
        self.widgetList.append(SimpleDropDown.SimpleDropDown(self.tabs[tabName], x, y))

    def createVideoWidget(self, tabName, x, y, widgetInfo):
        """Creates a video widget in the tab name specified"""
        self.widgetList.append(VideoWidget.VideoWidget(self.tabs[tabName], x, y, widgetInfo))

    def createCompassWidget(self, tabName, x, y, widgetInfo):
        """Creates a compass widget"""
        self.widgetList.append(CompassWidget(self.tabs[tabName], "compass{}".format(self.widgetsCreated), x, y, widgetInfo))
        self.widgetsCreated += 1

    def createTextBoxDropDownWidget(self, tabName, x, y):
        """Creates a textbox with a drop down in the tab name specified"""
        self.widgetList.append(TextBoxDropDownWidget.TextBoxDropDownWidget(self.tabs[tabName], "textBoxDropDown_{}".format(self.widgetsCreated), x, y))
        self.widgetsCreated = self.widgetsCreated + 1

    def getMainWindow(self):
        return self.mainWindow

    def getTabNames(self):
        """Returns a list of tab names IN ORDER!!!"""
        return self.tabNames
