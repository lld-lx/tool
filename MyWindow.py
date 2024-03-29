from sys import argv, exit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout
from my_tool.mitm import MiTm
from my_tool.mouse_keyboard import Record
from my_tool.search import DiyWindow, TipWindow
from qss.reader import CommonHelper
from win_fonts.move_font import MOVE
from qt_members.close_mini_max import CMM
from my_tool.browser_headers_change_to_dict import BrowserHeaders
from win_fonts.round_font import RoundShadow, FramelessWindow
from signals.create_signal import WinPos, WinCreate


class Tool(RoundShadow, MOVE, FramelessWindow):
    def __init__(self):
        super(Tool, self).__init__()
        self.read = CommonHelper().read_qss
        self._main_ui()  # 页面布局
        self.window()   # 窗口元素

    def _main_ui(self):
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QVBoxLayout()  # 创建水平布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为水平
        self.main_widget.setObjectName('main_widget')

        self.top_widget = QWidget()  # 创建上半部分的部件
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QGridLayout()  # 创建上半部分部件的网格布局层
        self.top_widget.setLayout(self.top_layout)  # 设置上半部分部件布局
        self.top_widget.setMouseTracking(True)

        self.top_left_widget = QWidget()
        self.top_left_widget.setObjectName('top_left_widget')
        self.top_left_layout = QGridLayout()  # 创建上部份左侧的网格布局层
        self.top_left_widget.setLayout(self.top_left_layout)  # 设置上部份左侧的布局

        self.top_right_widget = QWidget()
        self.top_right_widget.setObjectName('top_right_widget')
        self.top_right_layout = QHBoxLayout()  # 水平布局
        self.top_right_widget.setLayout(self.top_right_layout)  # 设置上部份右侧的布局

        self.under_widget = QWidget()  # 创建下半部份的部件
        self.under_widget.setObjectName('under_widget')
        self.under_layout = QVBoxLayout()  # 垂直布局
        self.under_widget.setLayout(self.under_layout)  # 设置下半部份布局
        self.under_widget.setMouseTracking(True)

        self.main_layout.addWidget(self.top_widget, 1)  # 上侧部件占比1
        self.main_layout.addWidget(self.under_widget, 5)  # 下侧部件占比5
        self.top_layout.addWidget(self.top_left_widget, 0, 0, 4, 10)
        self.top_layout.addWidget(self.top_right_widget, 0, 10, 4, 2)

        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)

    def window(self):
        """显示窗口"""
        self.resize(500, 500)
        for i, j in enumerate(CMM(self).circle_button()):
            self.top_right_layout.addWidget(j, 1, Qt.AlignTop)  # 关闭放大三个按钮
        BrowserHeaders(self.top_layout, self.under_layout)  # 表头工具
        self._slot()  # 创建信号槽
        DiyWindow(self, self.send)
        MiTm(self.top_layout, self.under_layout)
        Record(self.top_layout, self.under_layout)
        self.some_qss_set()
        self.show()

    def _slot(self):
        self.send = WinPos()  # 创建信号
        self.slot = WinCreate()  # 创建槽位
        self.send.send_msg.connect(self.slot.get)
        self.slot.set_object(TipWindow)

    def some_qss_set(self):
        widget_qss = self.read("./qss/top.qss")
        self.top_widget.setStyleSheet(widget_qss)
        self.under_widget.setStyleSheet(widget_qss)
        self.top_left_widget.setStyleSheet(widget_qss)
        self.top_right_widget.setStyleSheet(widget_qss)


if __name__ == '__main__':
    app = QApplication(argv)
    ex = Tool()
    exit(app.exec_())
