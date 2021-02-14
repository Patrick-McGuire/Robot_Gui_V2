"""
Probot Browse
"""

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

from .CustomBaseWidget import CustomBaseWidget
from Constants import Constants


class Browse(CustomBaseWidget):
    def __init__(self, tab, name, x, y, widgetInfo):
        self.web = QWebEngineView()
        self.linkEntry = QLineEdit()
        self.submit = QPushButton("Enter Link")
        self.defaultButton = QPushButton("Default")
        super().__init__(QWidget(tab, objectName=name), x, y, widgetType=Constants.BROWSE_TYPE)

        layout = QGridLayout()
        layout.addWidget(self.linkEntry, 0, 0)
        layout.addWidget(self.submit, 0, 1)
        layout.addWidget(self.defaultButton, 0, 2)
        layout.addWidget(self.web, 1, 0, 1, 3)
        self.QTWidget.setLayout(layout)

        self.submit.clicked.connect(self.goToURLFromEntryBox)
        self.defaultButton.clicked.connect(self.goToDefaultURL)

        self.setSize(800, 500)

        # Default Behavior
        if Constants.URL_ATTRIBUTE in widgetInfo:
            self.defaultURL = widgetInfo[Constants.URL_ATTRIBUTE]
            self.goToURL(self.defaultURL)
        else:
            self.defaultURL = None
            self.goToURL("www.google.com")

    def customUpdate(self, dataPassDict):
        pass

    def goToURL(self, url):
        """
        URL processing
        Should detect google searches, and should add https text
        """

        if url is None or len(str(url)) == 0:  # Just skip bad data
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

    def goToDefaultURL(self):
        self.goToURL(self.defaultURL)

    def customXMLStuff(self, tag):
        tag.set(Constants.URL_ATTRIBUTE, str(self.defaultURL))
