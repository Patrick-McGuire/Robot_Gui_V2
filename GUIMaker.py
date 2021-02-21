"""
Function calls to actually create GUI elements
"""

import types
import inspect

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget

from WidgetClasses import SimpleButton
from WidgetClasses import TextBoxWidget
from WidgetClasses import SimpleDropDown
from WidgetClasses import VideoWidget
from WidgetClasses import CompassWidget
from WidgetClasses import TextBoxDropDownWidget
from WidgetClasses import FrameRateCounter
from WidgetClasses import AnnunciatorPanel
from WidgetClasses import SimpleConsoleWidget
from WidgetClasses import CompleteConsoleWidget
from WidgetClasses import Browse


class GUIMaker(object):
    tabs = {}
    tabNames = []
    widgetList = []

    widgetClasses = {}  # Dictionary of widgetName: class

    def __init__(self):
        self.application = QApplication([])
        self.mainWindow = QMainWindow()
        self.mainWindow.setObjectName("Main_Window")
        self.application.setObjectName("Application")
        self.mainWindow.menuBar().setObjectName("Menu_Bar")

        self.tabHolderWidget = QTabWidget()
        self.tabHolderWidget.setObjectName("Tab_Holder")
        self.tabHolderWidget.tabBar().setObjectName("Tab_Bar")
        self.tabHolderWidget.resize(300, 200)

        self.widgetsCreated = 0

        for name, val in globals().items():  # Loop through globals()
            if isinstance(val, types.ModuleType) and "WidgetClasses" in str(val):  # Only look at modules from WidgetClasses
                for item in inspect.getmembers(val):
                    if name in str(item) and "__" not in str(item) and "FrameRateCounter" not in name:
                        self.widgetClasses[name] = item[1]

    def start(self):
        self.mainWindow.setCentralWidget(self.tabHolderWidget)

        self.mainWindow.show()
        self.application.exec_()

    def stop(self):
        print("Stopping GUI")
        self.application.exit()
        exit(0)

    def SetTitle(self, title):
        self.mainWindow.setWindowTitle(title)

    def setWindowGeometry(self, width, height):
        self.mainWindow.setGeometry(0, 0, int(width), int(height))

    def getWidgetList(self):
        return self.widgetList

    def createTab(self, name):
        """Creates a tab with the specified name"""
        self.tabs[name] = QWidget()
        self.tabs[name].setObjectName(name)

        self.tabHolderWidget.addTab(self.tabs[name], name)
        self.tabNames.append(name)

        self.createFrameRateCounterWidget(name, -100, -400)  # We need something on the tab to be updating if in order for the GUI to keep running

    def createButton(self, tabName, x, y, widgetInfo):
        """Creates a basic button widget in the tab name specified"""
        self.createWidgetFromName("SimpleButton", tabName, x, y, widgetInfo)

    def createTextBox(self, tabName, x, y, widgetInfo):
        """Creates a text box widget in the tab name specified"""
        self.widgetList.append(TextBoxWidget.TextBoxWidget(self.tabs[tabName], "compass{}".format(self.widgetsCreated), x, y, widgetInfo))
        self.widgetsCreated += 1

    def createSimpleDropDown(self, tabName, x, y):
        """Creates a text box widget in the tab name specified"""
        self.widgetList.append(SimpleDropDown.SimpleDropDown(self.tabs[tabName], "_", x, y, None))

    def createVideoWidget(self, tabName, x, y, widgetInfo):
        """Creates a video widget in the tab name specified"""
        self.widgetList.append(VideoWidget.VideoWidget(self.tabs[tabName], x, y, widgetInfo))

    def createCompassWidget(self, tabName, x, y, widgetInfo):
        """Creates a compass widget"""
        self.widgetList.append(CompassWidget.CompassWidget(self.tabs[tabName], "compass{}".format(self.widgetsCreated), x, y, widgetInfo))
        self.widgetsCreated += 1

    def createTextBoxDropDownWidget(self, tabName, x, y, widgetInfo=None):
        """Creates a textbox with a drop down in the tab name specified"""
        if widgetInfo is None:
            widgetInfo = {}
        self.widgetList.append(TextBoxDropDownWidget.TextBoxDropDownWidget(self.tabs[tabName], "textBoxDropDown_{}".format(self.widgetsCreated), x, y, widgetInfo))
        self.widgetsCreated = self.widgetsCreated + 1

    def createFrameRateCounterWidget(self, tabName, x, y):
        self.widgetList.append(FrameRateCounter.FrameRateCounter(self.tabs[tabName], x, y))

    def createAnnunciatorPanelWidget(self, tabName, x, y, widgetInfo=None):
        """Creates a textbox with a drop down in the tab name specified"""
        if widgetInfo is None:
            widgetInfo = {}
        self.widgetList.append(AnnunciatorPanel.AnnunciatorPanel(self.tabs[tabName], "annunciator_{}".format(self.widgetsCreated), x, y, widgetInfo))
        self.widgetsCreated = self.widgetsCreated + 1

    def createSimpleConsoleWidget(self, tabName, x, y, widgetInfo=None):
        """Creates a textbox with a drop down in the tab name specified"""
        if widgetInfo is None:
            widgetInfo = {}
        self.widgetList.append(SimpleConsoleWidget.SimpleConsole(self.tabs[tabName], "simple_console_{}".format(self.widgetsCreated), x, y, widgetInfo))
        self.widgetsCreated += 1

    def createCompleteConsoleWidget(self, tabName, x, y, widgetInfo=None):
        """Creates a textbox with a drop down in the tab name specified"""
        self.createWidgetFromName("CompleteConsoleWidget", tabName, x, y, widgetInfo)

    def createBrowse(self, tabName, x, y, widgetInfo=None):
        self.createWidgetFromName("Browse", tabName, x, y, widgetInfo)

    def createWidgetFromName(self, widgetName, tabName, x, y, widgetInfo=None):
        """Will create any widget from its file name!"""
        if widgetInfo is None:
            widgetInfo = {}

        try:
            self.widgetList.append(self.widgetClasses[widgetName](self.tabs[tabName], "{0}_{1}".format(widgetName, self.widgetsCreated), x, y, widgetInfo))
            self.widgetsCreated += 1
            return True
        except:
            print("Dynamically creating {} type widgets is not supported yet".format(widgetName))
            return False

    def getMainWindow(self):
        return self.mainWindow

    def getTabNames(self):
        """Returns a list of tab names IN ORDER!!!"""
        return self.tabNames

    def setGUIColor(self, red, green, blue):
        colorString = " background: rgb({0}, {1}, {2});".format(red, green, blue)
        slightlyDarkerColor = " background: rgb({0}, {1}, {2});".format(max(red - 10, 0), max(green - 10, 0), max(blue - 10, 0))

        if max(red, green, blue) > 127:
            textColorString = " color: black"
        else:
            textColorString = " color: white"

        self.mainWindow.setStyleSheet("QWidget#" + self.mainWindow.objectName() + "{" + slightlyDarkerColor + textColorString + "}")
        self.tabHolderWidget.setStyleSheet("QWidget#" + self.tabHolderWidget.objectName() + "{" + colorString + textColorString + "}")
        self.mainWindow.menuBar().setStyleSheet("QWidget#" + self.mainWindow.menuBar().objectName() + "{" + slightlyDarkerColor + textColorString + "}")
        self.tabHolderWidget.tabBar().setStyleSheet("QWidget#" + self.tabHolderWidget.tabBar().objectName() + "{" + slightlyDarkerColor + textColorString + "}")

        for tab in self.tabs:
            self.tabs[tab].setStyleSheet("QWidget#" + self.tabs[tab].objectName() + "{" + colorString + textColorString + "}")

    def getAvailableWidgets(self):
        return self.widgetClasses.keys()
