from threading import Thread
from queue import Queue

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor

from record_tool.record_main import listen_center
from record_tool.record_mouse import start_mouse_listen
from record_tool.record_keyboard import start_keyboard_listen

from PyQt5.QtWidgets import QPushButton, QTextEdit
from qt_members.tool_bar import ToolMember

show_que = Queue()


class MyTypeSignal(QObject):
    # 定义一个信号
    send_msg = pyqtSignal()

    def run(self):
        self.send_msg.emit()


class MySlot(QObject):
    text = None

    def set_object(self, text):
        self.text = text

    def get(self):
        self.text.clear()


class Record(ToolMember):

    def __init__(self, father, mother):
        super(Record, self).__init__(father, mother)
        self.textEdit = None
        self.start_button = None
        self.num = 0
        self.tool_bar()

    def tool_bar(self):
        self.any_bar(
            '鼠标键盘录制', './picture/headers.png',
            "record", lambda: self._tool_bar_click()
        )

    def _qt_text(self):
        self.qt = QTextEdit()
        self.cur = self.qt.textCursor()
        self.send = MyTypeSignal()  # 创建信号
        self.slot = MySlot()    # 创建槽位
        self.slot.set_object(self.qt)
        self.qt.setReadOnly(True)  # 设置只读

    def _qt_button(self):
        self.bu = QPushButton()
        self.bu.clicked.connect(lambda: self.start_record())

    def _tool_bar_click(self):
        self.remove()
        self._qt_text()
        self._qt_button()
        self.mother.addWidget(self.bu)
        self.mother.addWidget(self.qt)

    def _style(self, event, event_msg, time):
        """
        html
        """
        self.num += 1
        self.qt.moveCursor(QTextCursor.Start)
        self.qt.insertPlainText(self.html(event, event_msg, time))
        self.qt.insertPlainText(self.html(event, event_msg, time))

        self.cur.movePosition(QTextCursor.End, QTextCursor.MoveAnchor, 0)
        # self.cur.setPosition(0, QTextCursor.KeepAnchor)
        # self.cur.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor, 0)
        # self.cur.removeSelectedText()

    @staticmethod
    def html(event, event_msg, time):
        inner = "事件:%s  内容:%s  时间:%s\n" % (event, event_msg, time)
        return inner

    def start_record(self):
        Thread(target=listen_center).start()
        Thread(target=start_mouse_listen).start()
        Thread(target=start_keyboard_listen).start()
        Thread(target=self.get_result).start()

    def get_result(self):
        # 信号连接
        self.send.send_msg.connect(self.slot.get)
        while True:
            center = show_que.get()
            j = center.contents
            param = j.wParam
            if param == 256 or param == 257 or param == 260 or param == 261:
                self._style("键盘", j.k.contents.vkCode, j.k.contents.time)
            else:
                self._style("鼠标", param, j.m.contents.time)
            if self.num == 200:
                self.num = 0
                self.send.run()
