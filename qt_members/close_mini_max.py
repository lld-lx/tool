from PyQt5.QtWidgets import QGraphicsOpacityEffect, QWidget
from qss.reader import CommonHelper
from win_fonts.hover_set import MyButton


# 顶部按钮的样式
class CMM(QWidget):
    def __init__(self, father):
        self.read = CommonHelper().read_qss
        self.father = father
        self.is_max = 0
        self.animation = None
        super(CMM, self).__init__()

    # 圆形样式的按钮
    def circle_button(self):
        op = QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(0.9)
        # 创建关闭、缩小等按钮
        qtn_exit = MyButton('', self.father)
        qtn_full = MyButton('', self.father)
        qtn_mini = MyButton('', self.father)
        qtn_exit.setObjectName('top_button_exit')
        qtn_mini.setObjectName('top_button_mini')
        qtn_full.setObjectName('top_button_full')
        # 设置透明度
        qtn_exit.setGraphicsEffect(op)
        qtn_mini.setGraphicsEffect(op)
        qtn_full.setGraphicsEffect(op)
        # 设置提示文本
        qtn_exit.setToolTip('关闭')
        qtn_mini.setToolTip('缩小')
        qtn_full.setToolTip('放大')
        # 设置按钮大小
        qtn_exit.setFixedSize(15, 15)
        qtn_full.setFixedSize(15, 15)
        qtn_mini.setFixedSize(15, 15)
        # 设置样式
        qss = self.read('./qss/top.qss')
        qtn_exit.setStyleSheet(qss)
        qtn_mini.setStyleSheet(qss)
        qtn_full.setStyleSheet(qss)
        # 绑定事件槽
        qtn_exit.clicked.connect(self.father.close)
        qtn_exit.resize(qtn_exit.sizeHint())
        qtn_mini.clicked.connect(self.father.showMinimized)
        qtn_mini.resize(qtn_mini.sizeHint())
        qtn_full.clicked.connect(lambda: self.full_qtn(qtn_full))
        qtn_full.resize(qtn_full.sizeHint())

        return qtn_mini, qtn_full, qtn_exit

    def full_qtn(self, qtn_full):
        if self.is_max == 0:
            self.father.showMaximized()
            qtn_full.setToolTip("恢复")
            self.is_max = 1
        else:
            self.father.showNormal()
            qtn_full.setToolTip("放大")
            self.is_max = 0
