"""
Probot Browse
"""

import xml.etree.ElementTree as ElementTree

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class Browse(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.web = QWebEngineView()
        self.linkEntry = QLineEdit()
        self.submit = QPushButton("Enter Link")
        super().__init__(QWidget(tab, objectName=name), x, y)

        layout = QGridLayout()
        layout.addWidget(self.linkEntry, 0, 0)
        layout.addWidget(self.submit, 0, 1)
        layout.addWidget(self.web, 1, 0, 1, 2)
        self.QTWidget.setLayout(layout)

        self.submit.clicked.connect(self.goToURLFromEntryBox)

        self.setSize(800, 500)
        self.goToURL("www.google.com")

    def customUpdate(self, dataPassDict):
        pass

    def goToURL(self, url):
        """
        URL processing

        Should detect google searches, and should add https text
        """
        if len(url) == 0:
            return

        if "." not in url:
            url = "https://www.google.com/search?q=" + url
        elif url[0:8] != "https://" and url[0:7] != "http://":
            url = "https://" + url

        self.goToRawURL(url)

    def goToRawURL(self, url):
        self.linkEntry.setText(url)
        self.web.load(QUrl(url))

    def goToURLFromEntryBox(self):
        self.goToURL(self.linkEntry.text())
