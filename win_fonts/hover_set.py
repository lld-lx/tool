from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import Qt


class MyButton(QPushButton, QWidget):
    def __int__(self):
        super(MyButton, self).__init__()
        self.animation = None

    def enterEvent(self, e):  # 鼠标移入button
        QPushButton()
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, e):  # 鼠标移出button
        self.setCursor(QCursor(Qt.ArrowCursor))
