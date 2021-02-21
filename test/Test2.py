from PyQt5 import QtGui, QtWidgets


class TabBar(QtWidgets.QTabBar):
    def __init__(self, colors, parent=None):
        super(TabBar, self).__init__(parent)
        self.mColors = colors

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            if opt.text in self.mColors:
                opt.palette.setColor(
                    QtGui.QPalette.Button, self.mColors[opt.text]
                )
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        d = {
            "All": QtGui.QColor("yellow"),
            "purchase": QtGui.QColor("#87ceeb"),
            "POS Sales": QtGui.QColor("#90EE90"),
            "Cash Sales": QtGui.QColor("pink"),
            "invoice": QtGui.QColor("#800080"),
        }
        self.setTabBar(TabBar(d))

        self.addTab(QtWidgets.QLabel(), "All")
        self.addTab(QtWidgets.QLabel(), "purchase")
        self.addTab(QtWidgets.QLabel(), "POS Sales")
        self.addTab(QtWidgets.QLabel(), "Cash Sales")
        self.addTab(QtWidgets.QLabel(), "invoice")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = TabWidget()
    w.show()
    sys.exit(app.exec_())