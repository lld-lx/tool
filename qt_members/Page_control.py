from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.Qt import QIntValidator

'''
1、提供数据翻页显示接口
'''


class PageController(QWidget):
    def __init__(self):
        super(PageController).__init__()

    def _init_ui(self, page_layout):
        page_weight = QWidget()
        control_layout = QHBoxLayout()
        page_weight.setLayout(control_layout)

        self.prePage = QPushButton("<上一页")
        self.curPage = QLabel("1")
        self.nextPage = QPushButton("下一页>")

        self.totalPage = QLabel("共 " + str(self.page + 1) + " 页")
        skip_label_0 = QLabel("跳到")
        self.skipPage = QLineEdit()
        self.skipPage.setPlaceholderText("请输入跳转的页码")
        self.skipPage.setValidator(QIntValidator())  # 设置只能输入int类型的数据
        skip_label_1 = QLabel("页")
        self.confirmSkip = QPushButton("确定")
        control_layout.addStretch(1)
        control_layout.addWidget(self.prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(self.nextPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skip_label_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skip_label_1)
        control_layout.addWidget(self.confirmSkip)
        control_layout.addStretch(1)
        self.prePage.clicked.connect(lambda: self.button_clicked())
        self.nextPage.clicked.connect(lambda: self.button_clicked())
        self.confirmSkip.clicked.connect(lambda: self.button_clicked())

        page_layout.addWidget(page_weight, 9, 3, 1, 5)

    def button_clicked(self):
        button_text = self.mother.sender().text()
        total_page = int(self.totalPage.text().split()[1])
        current_page = int(self.curPage.text())

        if "<上一页" == button_text:
            self.skipPage.setText('')

            current_page = current_page - 1
            if current_page <= 1:
                self.curPage.setText('1')
            else:
                self.curPage.setText(str(current_page))
            self.page_switch()
            self.recover(current_page - 1)

        if "下一页>" == button_text:
            self.skipPage.setText('')
            current_page = current_page + 1
            if current_page <= total_page:
                self.curPage.setText(str(current_page))
            else:
                return
            self.recover(current_page - 1)

        if "确定" == button_text:
            if '' == self.skipPage.text():
                return

            page = int(self.skipPage.text())
            if 1 <= page <= total_page:
                self.curPage.setText(str(page))
            if page > total_page:
                self.curPage.setText(str(total_page))
                self.skipPage.setText(str(total_page))

            if page <= 0:
                self.curPage.setText(str(1))
                self.skipPage.setText(str(1))
            self.recover(current_page - 1)

    @property
    def PAGE(self):
        return int(self.totalPage.text().split()[1])

    @PAGE.setter
    def PAGE(self, page: int):
        if page < 0:
            return
        self.totalPage.setText("共 " + str(page) + " 页")
