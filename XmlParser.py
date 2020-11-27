"""
The old XML parser from the last GUI
"""

import xml.dom.minidom


class XmlParser:
    def __init__(self, filename, window):
        self.widgetsByTab = []
        self.tabData = []
        self.configInfo = []

        # Turn the file into a xml file
        self.document = xml.dom.minidom.parse(filename)

        # Get attributes that will apply to the entire window
        self.guiName = self.document.getElementsByTagName(Constants.WINDOW_NAME)[0].getAttribute(Constants.TITTLE_ATTRIBUTE)
        windowHeight = self.document.getElementsByTagName(Constants.WINDOW_NAME)[0].getAttribute(Constants.HEIGHT_ATTRIBUTE)
        windowWidth = self.document.getElementsByTagName(Constants.WINDOW_NAME)[0].getAttribute(Constants.WIDTH_ATTRIBUTE)

        self.guiGenerator.setWindowName(self.guiName)
        self.guiGenerator.setWindowSize(windowWidth, windowHeight)

        # Get all of the tabs from the file
        tabs = self.document.getElementsByTagName(Constants.TAB_NAME)

        # Generate all of the tabs
        for i in range(0, len(tabs)):
            # Add a new tab for every tab in the xml file
            tabName = tabs[i].getAttribute(Constants.TITTLE_ATTRIBUTE)
            self.guiGenerator.addTab(tabName)
            self.tabData.append([tabName])
            self.widgetsByTab.append([])

            # Get a list of widgets for the current tab
            widgets = tabs[i].getElementsByTagName(Constants.WIDGET_NAME)
            for widget in widgets:
                self.createWidget(widget, self.guiGenerator.getGuiTabs()[i + 1])
                self.widgetsByTab[i].append(self.guiGenerator.getAllWidgetsList()[-1])

    def createWidget(self, widget, tab):
        title = self.getAttribute(widget, Constants.TITTLE_ATTRIBUTE, "Error: no title")
        font = self.getAttribute(widget, Constants.FONT_ATTRIBUTE, "Arial")
        fontSize = self.getAttribute(widget, Constants.FONT_SIZE_ATTRIBUTE, "20")
        xPos = self.getAttribute(widget, Constants.X_POS_ATTRIBUTE, "0")
        yPos = self.getAttribute(widget, Constants.Y_POS_ATTRIBUTE, "0")
        foregroundColor = self.getAttribute(widget, Constants.FOREGROUND_ATTRIBUTE, "Black")
        backgroundColor = self.getAttribute(widget, Constants.BACKGROUND_ATTRIBUTE, "Light Grey")
        hidden = self.getAttribute(widget, Constants.HIDDEN_ATTRIBUTE, "False") == "True"
        draggable = self.getAttribute(widget, Constants.DRAGGABLE_ATTRIBUTE, "True") == "True"
        borderWidth = self.getAttribute(widget, Constants.BORDER_WIDTH_ATTRIBUTE, "4")
        relief = self.getAttribute(widget, Constants.RELIEF_ATTRIBUTE, "raised")

        widgetInfo = {
            Constants.TITTLE_ATTRIBUTE: title,
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

        # Code to handle specific types of widgets
        self.configInfo = []
        widgetType = widget.getAttribute(Constants.TYPE_ATTRIBUTE)
        if widgetType == Constants.CONFIGURABLE_TEXT_BOX_TYPE:
            lines = widget.getElementsByTagName(Constants.LINE_NAME)
            for line in lines:
                label = line.getAttribute(Constants.LABEL_ATTRIBUTE)
                value = line.getAttribute(Constants.VALUE_ATTRIBUTE)
                self.configInfo.append([label, value])

                self.dataPassDictionary[value] = 0

            widgetInfo[Constants.CONFIG_ATTRIBUTE] = self.configInfo
            self.guiGenerator.createConfigurableTextBox(widgetInfo)
        elif widgetType == Constants.VIDEO_WINDOW_TYPE:
            widgetInfo[Constants.SOURCE_ATTRIBUTE] = self.getAttribute(widget, Constants.SOURCE_ATTRIBUTE, "webcam")
            widgetInfo[Constants.DIMENSIONS_ATTRIBUTE] = self.getAttribute(widget, Constants.DIMENSIONS_ATTRIBUTE, "800x600")
            widgetInfo[Constants.FULLSCREEN_ATTRIBUTE] = self.getAttribute(widget, Constants.FULLSCREEN_ATTRIBUTE, "False")
            widgetInfo[Constants.LOCK_ASPECT_RATIO_ATTRIBUTE] = self.getAttribute(widget, Constants.LOCK_ASPECT_RATIO_ATTRIBUTE, "True")

            # Define data pass values needed
            self.dataPassDictionary[widgetInfo[Constants.SOURCE_ATTRIBUTE]] = 0

            self.guiGenerator.createVideoWindow(widgetInfo)
        elif widgetType == Constants.COMPASS_TYPE:
            widgetInfo[Constants.SIZE_ATTRIBUTE] = self.getAttribute(widget, Constants.SIZE_ATTRIBUTE, "200")
            widgetInfo[Constants.SOURCE_ATTRIBUTE] = self.getAttribute(widget, Constants.SOURCE_ATTRIBUTE, "bruh")
            self.dataPassDictionary[widgetInfo[Constants.SOURCE_ATTRIBUTE]] = 0
            self.guiGenerator.createCompass(widgetInfo)
        elif widgetType == "ConfigurableGraph":
            lines = widget.getElementsByTagName(Constants.LINE_NAME)
            for line in lines:
                label = line.getAttribute(Constants.LABEL_ATTRIBUTE)
                value = line.getAttribute(Constants.VALUE_ATTRIBUTE)
                self.configInfo.append([label, value])

                self.dataPassDictionary[value] = 0

            widgetInfo[Constants.CONFIG_ATTRIBUTE] = self.configInfo
            self.guiGenerator.createConfigurableGraph(widgetInfo)
        else:
            print("Could not create widget {0}: type {1} not supported".format(title, widgetType))

    def getAttribute(self, xmlClip, attribute, default):
        data = xmlClip.getAttribute(attribute)
        if data == "":
            return default
        return data

    def getDataPassDictionary(self):
        return self.dataPassDictionary

    def getAllWidgetsList(self):
        return self.guiGenerator.getAllWidgetsList()

    def getConfigInfo(self):
        return self.configInfo

    def getGuiName(self):
        return self.guiName

    def getTabInfo(self):
        return self.tabData

    def getWidgetsByTab(self):
        return self.widgetsByTab
