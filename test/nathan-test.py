from PyQt5.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    app = QApplication([])
    label = QLabel('Hello World!')
    label.show()
    app.exec_()
