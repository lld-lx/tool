"""继承了QLineEdit,重新定义实现部分功能"""
from PyQt5.QtWidgets import QLineEdit


class LineEdit(QLineEdit):

    def __init__(self, text):
        super(LineEdit, self).__init__()
        # 绑定text_changed事件,将改变的值写入传入的list中
        self.save_text = text
        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.save_text.clear()
        self.save_text.append(self.text())
