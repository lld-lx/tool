from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(1, 9)


class MOVE(QWidget):
    Margins = 15
    """重写Qt的移动类"""
    def __init__(self):
        super(MOVE, self).__init__()  # 继承QWidget,这会创建一个窗口,对象赋给self
        self.setMouseTracking(True)
        self._endPos, self._startPos, self._tracking = None, None, None
        self._mpos = None
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        super(MOVE, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed and self.Direction:
            self._resizeWidget(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # 右上角
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif wm >= xPos >= self.Margins >= yPos >= 0:
            # 上面
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and self.Margins <= yPos <= hm:
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
        if self._tracking:
            self._endPos = pos - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, event):
        super(MOVE, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True
            self._startPos = QPoint(event.x(), event.y())
            self._tracking = True

    def mouseReleaseEvent(self, event):
        super(MOVE, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

        if event.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        if self.Direction is None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()

        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        if self.Direction == LeftTop:  # 左上角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:  # 右下角
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == RightTop:  # 右上角
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == LeftBottom:  # 左下角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == Left:  # 左边
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:  # 右边
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == Top:  # 上面
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:  # 下面
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return

        self.setGeometry(x, y, w, h)
        self.setCursor(Qt.ArrowCursor)
