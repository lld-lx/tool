from PyQt5.QtCore import QObject, pyqtSignal


class MyTypeSignal(QObject):
    # 定义一个信号
    send_msg = pyqtSignal()

    def run(self):
        self.send_msg.emit()


class WinPos(QObject):
    # 定义一个信号
    send_msg = pyqtSignal([int, int])

    def run(self, x, y):
        self.send_msg.emit(x, y)


class MySlot(QObject):
    text = None

    def set_object(self, text):
        self.text = text

    def get(self):
        self.text.clear()


class WinCreate(QObject):
    obj = None

    def set_object(self, obj):
        self.obj = obj

    def get(self, x, y):
        obj = self.obj(x, y)
        obj.exec()
