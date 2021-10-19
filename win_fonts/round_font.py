from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPropertyAnimation

Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class RoundShadow(QWidget):
    """圆角边框类"""
    def __init__(self):

        super(RoundShadow, self).__init__()
        self.border_width = 8
        # # 设置 窗口无边框和背景透明 *必须
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

    # def paintEvent(self, event):
    #     # 阴影
    #     path = QPainterPath()
    #     path.setFillRule(Qt.WindingFill)
    #
    #     pat = QPainter(self)
    #     pat.setRenderHint(pat.Antialiasing)
    #     pat.fillPath(path, QBrush(Qt.white))
    #
    #     color = QColor(192, 192, 192, 50)
    #
    #     for i in range(10):
    #         i_path = QPainterPath()
    #         i_path.setFillRule(Qt.WindingFill)
    #         ref = QRectF(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2)
    #         # i_path.addRect(ref)
    #         i_path.addRoundedRect(ref, self.border_width, self.border_width)
    #         color.setAlpha(int(150 - i**0.5*50))
    #         pat.setPen(color)
    #         pat.drawPath(i_path)


class FramelessWindow(QWidget):

    def __init__(self, *args, **kwargs):
        self.animation = None
        self.start = None
        super(FramelessWindow, self).__init__(*args, **kwargs)

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(FramelessWindow, self).move(pos)

    def showMaximized(self):
        """最大化,要去除上下左右边界,如果不去除则边框地方会有空隙"""
        super(FramelessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """还原,要保留上下左右边界,否则没有边框无法调整"""
        super(FramelessWindow, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

    def closeEvent(self, event):
        if self.animation is None:
            self.animation = QPropertyAnimation(self, b'windowOpacity')
            self.animation.setDuration(200)
            self.animation.setStartValue(1)
            self.animation.setEndValue(0)
            self.animation.start()
            self.animation.finished.connect(self.close)
            event.ignore()

    def showEvent(self, event):
        if self.start is None:
            self.start = True
            self.start = QPropertyAnimation(self, b'windowOpacity')
            self.start.setDuration(200)
            self.start.setStartValue(0)
            self.start.setEndValue(0.95)
            self.start.start()
            self.start.finished.connect(self.show)



