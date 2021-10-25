from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
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
        control_layout.addStretch(0)
        control_layout.addWidget(self.prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(self.nextPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addStretch(0)
        self.prePage.clicked.connect(lambda: self.button_clicked())
        self.nextPage.clicked.connect(lambda: self.button_clicked())

        page_layout.addWidget(page_weight, 10, 24, 1, 6)

    def button_clicked(self):
        button_text = self.mother.sender().text()
        total_page = int(self.totalPage.text().split()[1])
        current_page = int(self.curPage.text())

        if "<上一页" == button_text:
            current_page = current_page - 1
            if current_page == 0:
                return
            self.page_switch()
            self.curPage.setText(str(current_page))
            self.recover(current_page - 1)

        if "下一页>" == button_text:
            current_page = current_page + 1
            self.page_switch()
            if current_page <= total_page:
                self.curPage.setText(str(current_page))
            else:
                return
            self.recover(current_page - 1)
