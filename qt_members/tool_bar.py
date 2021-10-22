"""封装创建工具栏时需要重复使用的方法"""
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton, QWidget

from css.reader import CommonHelper


class ToolMember(QWidget):
    def __init__(self, father, mother):
        super(ToolMember).__init__()
        self.father = father
        self.mother = mother
        self.qss = CommonHelper().read_qss("./css/tool.qss")

    def any_bar(self, tip, picture, object_name, func):
        tool_button = QToolButton()
        tool_button.setToolTip(tip)
        tool_button.setIcon(QIcon(picture))  # 设置按钮图标
        tool_button.setIconSize(QSize(25, 30))  # 设置图标大小
        tool_button.setObjectName(object_name)
        tool_button.setStyleSheet(self.qss)
        tool_button.clicked.connect(func)
        self.father.addWidget(tool_button)

    def remove(self):
        item_list = list(range(self.mother.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序
        print(item_list)

        for i in item_list:
            item = self.mother.itemAt(i)
            self.mother.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
