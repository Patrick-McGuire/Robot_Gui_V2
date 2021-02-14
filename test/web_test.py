from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
win = QWidget()
web = QWebEngineView()
linkEntry = QLineEdit()
submit = QPushButton("Enter Link", win)

topLayout = QGridLayout()
layout = QGridLayout()

top = QWidget()
topLayout.addWidget(linkEntry, 0, 0)
topLayout.addWidget(submit, 0, 1)
topLayout.setAlignment(Qt.AlignTop)

top.setLayout(topLayout)

layout.addWidget(top, 0, 0)
layout.addWidget(web, 1, 0)

win.setLayout(layout)

layout.setAlignment(Qt.AlignTop)

web.setFixedHeight(900)


def gotoURL():
    web.load(QUrl(linkEntry.text()))


submit.clicked.connect(gotoURL)

win.setWindowTitle("Probot Browse")
win.show()

sys.exit(app.exec_())
