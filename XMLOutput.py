import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.etree import ElementTree

from Constants import *


class XMLOutput:
    def __init__(self, windowInfo, tabNames, widgetList, filename, excludeSettingsTab):
        self.windowInfo = windowInfo
        self.tabNames = tabNames
        self.widgetList = widgetList

        self.excludeSettingsTab = excludeSettingsTab

        self.getWindowStartTag()
        self.getTabTags()

        outFile = open(filename, "w")
        outFile.write(self.cleanUp(self.fileData))

    def getWindowStartTag(self):
        self.guiName = self.windowInfo[0]
        self.guiSize = [str(self.windowInfo[1]), str(self.windowInfo[2])]

        self.fileData = ET.Element(Constants.WINDOW_NAME)
        self.fileData.set(Constants.TITLE_ATTRIBUTE, self.guiName)
        self.fileData.set(Constants.WIDTH_ATTRIBUTE, self.guiSize[0])
        self.fileData.set(Constants.HEIGHT_ATTRIBUTE, self.guiSize[1])
        self.fileData.set(Constants.THEME_ATTRIBUTE, self.windowInfo[3])

    def getTabTags(self):
        items = []
        for tab in self.tabNames:
            if self.excludeSettingsTab and tab == "Settings":
                pass  # Don't save this tab
            else:
                items.append(ET.SubElement(self.fileData, Constants.TAB_NAME))
                items[-1].set(Constants.TITLE_ATTRIBUTE, tab)

                for widget in self.widgetList:
                    if widget.getTabName() == tab:
                        try:
                            widget.getXMLStuff(items[-1])
                        except AttributeError as e:
                            print(e)
                            print("Can't save {0}: no xml output method".format(widget))

    def cleanUp(self, elem):
        """Make data pretty"""
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return str(reparsed.toprettyxml(indent="\t"))
