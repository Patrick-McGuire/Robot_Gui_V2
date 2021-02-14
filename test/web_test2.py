from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

web = QWebEngineView()
web.load(QUrl("https://pythonspot.com"))
web.show()

sys.exit(app.exec_())
