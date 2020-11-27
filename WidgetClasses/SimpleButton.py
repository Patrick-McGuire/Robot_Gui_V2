"""
Text box widget
"""

from PyQt5.QtWidgets import QPushButton

from .CustomBaseWidget import CustomBaseWidget


class SimpleButton(CustomBaseWidget):
    def __init__(self, tab, buttonText, xPos, yPos):
        QTWidget = QPushButton(tab, text=buttonText)
        super().__init__(QTWidget, xPos, yPos)
