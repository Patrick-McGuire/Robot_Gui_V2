import os
import cv2

from PyQt5.QtWidgets import QLabel, QWidget

from WidgetClasses.WidgetHelpers import BasicImageDisplay


class CompassDisplayWidget(QLabel):
    def __init__(self, parentWidget: QWidget):
        self.imageLoaded = False

        super().__init__(parentWidget)

        self.size = 200

        dirName = os.path.dirname(__file__)
        dirName = os.path.abspath(os.path.join(dirName, "../.."))
        compass = cv2.imread("{}/Assets/compass.png".format(dirName), cv2.IMREAD_UNCHANGED)
        arrowImg = cv2.resize(cv2.imread("{}/Assets/arrow.png".format(dirName), cv2.IMREAD_UNCHANGED)[900:2100, 900:2100], (self.size, int(self.size / 2)))

        self.compassImage = BasicImageDisplay.BasicImageDisplay(self, compass, self.size)
        self.arrowImage = BasicImageDisplay.BasicImageDisplay(self, arrowImg, self.size)

        self.imageLoaded = True

    def setYaw(self, yaw):
        self.arrowImage.setRotation(yaw)

    def setSize(self, size):
        # TODO: Use the QWidget size functions instead of this sketchy one
        self.size = size

        self.setGeometry(0, 0, size, size)
        self.compassImage.setGeometry(size * 1)
        self.arrowImage.setGeometry(size * 1)
