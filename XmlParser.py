"""
The old XML parser from the last GUI
"""

import xml.dom.minidom

from GUIMaker import GUIMaker
from Constants import Constants


class XmlParser:
    def __init__(self, filename, GUICreater: GUIMaker):
        self.guiGenerator = GUICreater

        # Turn the file into a xml file
        self.document = xml.dom.minidom.parse(filename)

        # Get attributes that will apply to the entire window
        self.guiName = self.document.getElementsByTagName(Constants.WINDOW_NAME)[0].getAttribute(Constants.TITLE_ATTRIBUTE)
        windowHeight = self.document.getElementsByTagName(Constants.WINDOW_NAME)[0].getAttribute(Constants.HEIGHT_ATTRIBUTE)
        windowWidth = self.document.getElementsByTagName(Constants.WINDOW_NAME)[0].getAttribute(Constants.WIDTH_ATTRIBUTE)
        self.theme = self.document.getElementsByTagName(Constants.WINDOW_NAME)[0].getAttribute(Constants.THEME_ATTRIBUTE)

        self.guiGenerator.SetTitle(self.guiName)
        self.guiGenerator.setWindowGeometry(windowWidth, windowHeight)

        # Get all of the tabs from the file
        tabs = self.document.getElementsByTagName(Constants.TAB_NAME)
        self.listOfTabNames = []

        # Generate all of the tabs
        for i in range(0, len(tabs)):
            # Add a new tab for every tab in the xml file
            tabName = tabs[i].getAttribute(Constants.TITLE_ATTRIBUTE)
            self.listOfTabNames.append(tabName)
            self.guiGenerator.createTab(tabName)

            # Get a list of widgets for the current tab
            widgets = tabs[i].getElementsByTagName(Constants.WIDGET_NAME)
            for widget in widgets:
                self.createWidget(widget, tabName)

    def createWidget(self, widget, tab):
        title = self.getAttribute(widget, Constants.TITLE_ATTRIBUTE, "Error: no title")
        font = self.getAttribute(widget, Constants.FONT_ATTRIBUTE, "Arial")
        fontSize = self.getAttribute(widget, Constants.FONT_SIZE_ATTRIBUTE, "12")
        xPos = int(float(self.getAttribute(widget, Constants.X_POS_ATTRIBUTE, "0")))
        yPos = int(float(self.getAttribute(widget, Constants.Y_POS_ATTRIBUTE, "0")))
        foregroundColor = self.getAttribute(widget, Constants.FOREGROUND_ATTRIBUTE, "Black")
        backgroundColor = self.getAttribute(widget, Constants.BACKGROUND_ATTRIBUTE, "Light Grey")
        hidden = self.getAttribute(widget, Constants.HIDDEN_ATTRIBUTE, "False") == "True"
        draggable = self.getAttribute(widget, Constants.DRAGGABLE_ATTRIBUTE, "True") == "True"
        borderWidth = self.getAttribute(widget, Constants.BORDER_WIDTH_ATTRIBUTE, "4")
        relief = self.getAttribute(widget, Constants.RELIEF_ATTRIBUTE, "raised")

        widgetInfo = {
            Constants.TITLE_ATTRIBUTE: title,
            Constants.FONT_ATTRIBUTE: font,
            Constants.TAB_ATTRIBUTE: tab,
            Constants.FONT_SIZE_ATTRIBUTE: fontSize,
            Constants.X_POS_ATTRIBUTE: xPos,
            Constants.Y_POS_ATTRIBUTE: yPos,
            Constants.HIDDEN_ATTRIBUTE: hidden,
            Constants.DRAGGABLE_ATTRIBUTE: draggable,
            Constants.FOREGROUND_ATTRIBUTE: foregroundColor,
            Constants.BACKGROUND_ATTRIBUTE: backgroundColor,
            Constants.BORDER_WIDTH_ATTRIBUTE: borderWidth,
            Constants.RELIEF_ATTRIBUTE: relief
        }

        for item in widget.attributes.items():  # Get every xml item for a particular widget
            widgetInfo[item[0]] = item[1]

        # Code to handle specific types of widgets
        configInfo = []
        widgetType = widget.getAttribute(Constants.TYPE_ATTRIBUTE)
        widgetClassName = widgetType

        if widgetType == Constants.CONFIGURABLE_TEXT_BOX_TYPE:
            lines = widget.getElementsByTagName(Constants.LINE_NAME)
            for line in lines:
                label = line.getAttribute(Constants.LABEL_ATTRIBUTE)
                value = line.getAttribute(Constants.VALUE_ATTRIBUTE)
                configInfo.append([label, value])

            widgetInfo[Constants.CONFIG_ATTRIBUTE] = configInfo
            self.guiGenerator.createTextBox(tab, int(xPos), int(yPos), widgetInfo)
        else:  # Any one-line xml widget should go in here
            if widgetType == Constants.VIDEO_WINDOW_TYPE:  # Fix a couple widget name -> class name errors
                widgetClassName = "VideoWidget"
            elif widgetType == Constants.COMPASS_TYPE:
                widgetClassName = "CompassWidget"
            elif widgetType == Constants.DROP_DOWN_TEXT_BOX_TYPE:
                widgetClassName = "TextBoxDropDownWidget"
            elif widgetType == Constants.SIMPLE_CONSOLE_TYPE:
                widgetClassName = "SimpleConsoleWidget"
            elif widgetType == Constants.COMPLETE_CONSOLE_TYPE:
                widgetClassName = "CompleteConsoleWidget"
            elif widgetType == Constants.FULL_FLIGHT_TYPE:
                configInfo.append(widget.getElementsByTagName("compass"))
                configInfo.append(widget.getElementsByTagName("attitude"))
                configInfo.append(widget.getElementsByTagName("vSpeed"))
                configInfo.append(widget.getElementsByTagName("terrainAlt"))
                configInfo.append(widget.getElementsByTagName("altitude"))
                configInfo.append(widget.getElementsByTagName("groundSpeed"))
                widgetInfo[Constants.CONFIG_ATTRIBUTE] = configInfo
            elif widgetType == Constants.MULTI_GRAPH_TYPE:  # Multi-graphs have more configuration
                lines = widget.getElementsByTagName(Constants.LINE_NAME)
                for line in lines:
                    graphType = line.getAttribute(Constants.TYPE_ATTRIBUTE)
                    source = line.getAttribute(Constants.SOURCE_ATTRIBUTE)
                    title = line.getAttribute(Constants.TITLE_ATTRIBUTE)
                    minValue = line.getAttribute(Constants.MIN_ATTRIBUTE)
                    maxValue = line.getAttribute(Constants.MAX_ATTRIBUTE)
                    color = line.getAttribute(Constants.COLOR_ATTRIBUTE)
                    configInfo.append([graphType, source, title, minValue, maxValue, color])

                widgetInfo[Constants.CONFIG_ATTRIBUTE] = configInfo

            if not self.guiGenerator.createWidgetFromName(widgetClassName, tab, int(xPos), int(yPos), widgetInfo):
                print("XML Parser could not create widget {0}: type {1} not supported".format(title, widgetType))

    def getAttribute(self, xmlClip, attribute: str, default: str):
        data = xmlClip.getAttribute(attribute)
        if data == "":
            return default
        return data

    def getConfigData(self):
        return {Constants.THEME_ATTRIBUTE: self.theme, "tabNames": self.listOfTabNames}
