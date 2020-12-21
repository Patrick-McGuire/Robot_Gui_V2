"""
Text box widget
"""

import xml.etree.ElementTree as ElementTree

from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class AnnunciatorPanel(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        widgetInfo[Constants.FONT_ATTRIBUTE] = "Monospace"  # Forcing a monospace font fixes some formatting
        super().__init__(QWidget(tab), x, y, configInfo=widgetInfo, widgetType=Constants.ANNUNCIATOR_TYPE)
        self.QTWidget.setObjectName(name)

        self.xBuffer = 0
        self.yBuffer = 0

        layout = QGridLayout()
        self.annunciatorWidgets = []

        for i in range(10):
            self.annunciatorWidgets.append(QLabel())
            layout.addWidget(self.annunciatorWidgets[i])
        self.QTWidget.setLayout(layout)

    def customUpdate(self, dataPassDict):
        if "annunciator" not in dataPassDict:
            return

        data = dataPassDict["annunciator"]
        # print(data)

        for i in range(len(data)):
            self.annunciatorWidgets[i].setText(data[i][0])
            self.annunciatorWidgets[i].setToolTip(data[i][2])
            self.annunciatorWidgets[i].setToolTipDuration(5000)

            status = str(data[i][1])
            if status == "0":
                self.annunciatorWidgets[i].setStyleSheet("background: green; color: black")
            elif status == "1":
                self.annunciatorWidgets[i].setStyleSheet("background: yellow; color: black")
            elif status == "2":
                self.annunciatorWidgets[i].setStyleSheet("background: red; color: black")
            else:
                self.annunciatorWidgets[i].setStyleSheet("background: blue; color: black")

        self.QTWidget.adjustSize()

    # def customXMLStuff(self, tag):
    #     pass
