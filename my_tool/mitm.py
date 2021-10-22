"""自动启动一个mitmproxy程序，简化代码工作"""
from PyQt5.QtGui import QIcon

from qt_members.Page_control import PageController
from qt_members.tool_bar import ToolMember
from win_fonts.my_line_edit import LineEdit
from win_fonts.my_combo_box import ComboBox
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QGridLayout
from mitm_tool.proxy_set import proxy_start
from mitm_tool.create_addon import HTTP
from mitm_tool.mitm_start import mitmproxy_config, mitmproxy_start, mitmproxy_shutdown


# 实现页面、mitmproxy功能，继承父类的工具栏方法
class MiTm(ToolMember, PageController):
    def __init__(self, father, mother):
        super(MiTm, self).__init__(father, mother)
        self.father = father
        self.mother = mother
        self.config = None

        self.code_list = [None]
        self.ip_list, self.port_list = [None], [None]
        self.url_list, self.url_comb = [None], [None]
        self.rhe_list, self.rhe_comb = [None], [None]
        self.rda_list, self.rda_comb = [None], [None]
        self.she_list, self.she_comb = [None], [None]
        self.sda_list, self.sda_comb = [None], [None]
        self.all_msg = []

        self.code_text = None
        self.ip_text, self.port_text = None, None
        self.url_text, self.url_combo = None, None
        self.request_header_text, self.request_header_combo = None, None
        self.request_data_text, self.request_data_combo = None, None
        self.response_header_text, self.response_header_combo = None, None
        self.response_data_text, self.response_data_combo = None, None

        self.tool_bar()
        self.page = 0
        self.is_close = 1
        self.body_widget = QWidget()
        self.body_layout = QGridLayout()

    def tool_bar(self):
        self.any_bar(
            'mitmproxy监听', './picture/headers.png',
            "mitm_bar", lambda: self.tool_bar_click()
        )

    def tool_bar_click(self):
        self.remove()
        self.page_add_delete()
        self.tool_body()
        self._init_ui(self.body_layout)

    def page_add_delete(self):
        page_add = QPushButton()
        page_delete = QPushButton()
        page_add.setText("+")
        page_delete.setText("-")
        page_add.clicked.connect(lambda: self.page_index_plus(page_delete))
        page_delete.clicked.connect(lambda: self.page_index_sub(page_delete))
        page_delete.hide()
        self.body_layout.addWidget(page_add, 0, 5, 1, 1)
        self.body_layout.addWidget(page_delete, 0, 6, 1, 1)

    def tool_body(self):
        self.body_widget.setObjectName('mitm_body_widget')
        self.body_widget.setLayout(self.body_layout)  # 设置上半部分部件布局
        self.body_widget.setMouseTracking(True)

        ip_label = QLabel()
        ip_label.setText("ip:")
        ip_label.setToolTip("启动代理使用的ip地址")
        self.ip_text = LineEdit(self.ip_list)
        self.ip_text.setText('127.0.0.1')
        self.ip_text.setMaxLength(15)

        port_label = QLabel()
        port_label.setText("port:")
        port_label.setToolTip("启动代理使用的端口号")
        self.port_text = LineEdit(self.port_list)
        self.port_text.setText('8088')
        self.port_text.setMaxLength(5)

        url_label = QLabel()
        url_label.setText("url:")
        url_label.setToolTip("监听的url")
        self.url_text = LineEdit(self.url_list)
        self.url_combo = ComboBox(self.url_comb)
        self.url_combo.addItems(["全匹配", "正则匹配"])

        request_header_label = QLabel()
        request_header_label.setText("请求header:")
        request_header_label.setToolTip("需要篡改的请求头")
        self.request_header_text = LineEdit(self.rhe_list)
        self.request_header_combo = ComboBox(self.rhe_comb)
        self.request_header_combo.addItems(["字典匹配", "全匹配", "正则匹配"])

        request_data_label = QLabel()
        request_data_label.setText("请求body:")
        request_data_label.setToolTip("需要篡改的请求体")
        self.request_data_text = LineEdit(self.rda_list)
        self.request_data_combo = ComboBox(self.rda_comb)
        self.request_data_combo.addItems(["字典匹配", "全匹配", "正则匹配"])

        response_header_label = QLabel()
        response_header_label.setText("响应header:")
        response_header_label.setToolTip("需要篡改的响应头")
        self.response_header_text = LineEdit(self.she_list)
        self.response_header_combo = ComboBox(self.she_comb)
        self.response_header_combo.addItems(["字典匹配", "全匹配", "正则匹配"])

        response_data_label = QLabel()
        response_data_label.setText("响应body:")
        response_data_label.setToolTip("需要篡改的响应体")
        self.response_data_text = LineEdit(self.sda_list)
        self.response_data_combo = ComboBox(self.sda_comb)
        self.response_data_combo.addItems(["字典匹配", "全匹配", "正则匹配"])

        code_label = QLabel()
        code_label.setText("code:")
        code_label.setToolTip("设置非2xx连接代理时就断开连接")
        self.code_text = LineEdit(self.code_list)
        self.code_text.setMaxLength(4)
        code_label.hide()
        self.code_text.hide()
        more_button = QPushButton()
        self.more_click(more_button, code_label)
        more_button.clicked.connect(lambda: self.more_click(more_button, code_label))
        more_label = QLabel()
        more_label.setText("其他可选项")

        self.body_layout.addWidget(ip_label, 1, 1, 1, 1)
        self.body_layout.addWidget(self.ip_text, 1, 2, 1, 2)
        self.body_layout.addWidget(port_label, 1, 4, 1, 1)
        self.body_layout.addWidget(self.port_text, 1, 5, 1, 2)
        self.body_layout.addWidget(url_label, 2, 1, 1, 1)
        self.body_layout.addWidget(self.url_text, 2, 2, 1, 2)
        self.body_layout.addWidget(self.url_combo, 2, 4, 1, 1)
        self.body_layout.addWidget(request_header_label, 3, 1, 1, 1)
        self.body_layout.addWidget(self.request_header_text, 3, 2, 1, 2)
        self.body_layout.addWidget(self.request_header_combo, 3, 4, 1, 1)
        self.body_layout.addWidget(request_data_label, 4, 1, 1, 1)
        self.body_layout.addWidget(self.request_data_text, 4, 2, 1, 2)
        self.body_layout.addWidget(self.request_data_combo, 4, 4, 1, 1)
        self.body_layout.addWidget(response_header_label, 5, 1, 1, 1)
        self.body_layout.addWidget(self.response_header_text, 5, 2, 1, 2)
        self.body_layout.addWidget(self.response_header_combo, 5, 4, 1, 1)
        self.body_layout.addWidget(response_data_label, 6, 1, 1, 1)
        self.body_layout.addWidget(self.response_data_text, 6, 2, 1, 2)
        self.body_layout.addWidget(self.response_data_combo, 6, 4, 1, 1)
        self.body_layout.addWidget(more_button, 7, 1, 1, 1)
        self.body_layout.addWidget(more_label, 7, 2, 1, 1)
        self.body_layout.addWidget(code_label, 8, 1, 1, 1)
        self.body_layout.addWidget(self.code_text, 8, 2, 1, 1)

        self.mother.addWidget(self.body_widget)

    # 从面板中读取输入参数
    def start_mitmproxy(self, choose):
        ip = ...
        port = ...
        proxy_start(ip, port)  # 启动代理
        # 从面板输入中读取相关配置信息,每页为一组
        pages = ...
        addons = []
        for one_page in pages:
            addons.append(HTTP(one_page))

        self.config = mitmproxy_config(ip, port, addons)
        mitmproxy_start(self.config)

    def end_mitmproxy(self):
        mitmproxy_shutdown(self.config)

    def more_click(self, more_button, code_label):
        if self.is_close:
            more_button.setIcon(QIcon("./picture/closed.png"))
            code_label.hide()
            self.code_text.hide()
            self.is_close = 0
        else:
            more_button.setIcon(QIcon("./picture/open.png"))
            code_label.show()
            self.code_text.show()
            self.is_close = 1

    def page_index_plus(self, page_delete):
        self.page += 1
        self.totalPage.setText("共 " + str(self.page + 1) + " 页")
        if int(self.curPage.text()) == self.page:
            self.curPage.setText(str(int(self.curPage.text()) + 1))
        self.save_msg()
        if self.page:
            page_delete.show()
        print("添加后%s" % self.all_msg)

    def page_index_sub(self, page_delete):
        self.page -= 1
        self.totalPage.setText("共 " + str(self.page + 1) + " 页")
        if int(self.curPage.text()) == self.page + 2:
            self.curPage.setText(str(int(self.curPage.text()) - 1))
        if not self.page:
            page_delete.hide()
        self.recover(self.page)
        self.all_msg.pop()
        print("删除后%s" % self.all_msg)

    def save_msg(self):
        print("all: %s" % len(self.all_msg))
        print("page: %s" % (self.page + 1))
        # 解决无限加的问题
        if len(self.all_msg) == self.page + 1:
            return
        else:
            if self.page + 1 != int(self.curPage.text()):
                self.all_msg.append(
                    (
                        ('', ''),
                        (None, 0),
                        (None, 0),
                        (None, 0),
                        (None, 0),
                        (None, 0),
                        None
                    )
                )
            else:
                self.all_msg.append(
                    self.read_msg()
                )
        self.clear_control()

    def page_switch(self):
        if len(self.all_msg) < self.page + 1:
            self.all_msg.append(
                self.read_msg()
            )
        elif int(self.curPage.text()) - 1 <= self.page + 1:
            self.all_msg[int(self.curPage.text()) - 1] = (
                self.read_msg()
            )
        self.clear_control()

    def recover(self, page):
        print("翻页后%s" % self.all_msg)
        if self.all_msg[page][0][0] is not None:
            self.ip_text.setText(self.all_msg[page][0][0])
        if self.all_msg[page][0][1] is not None:
            self.port_text.setText(self.all_msg[page][0][1])
        if self.all_msg[page][1][0] is not None:
            self.url_text.setText(self.all_msg[page][1][0])
        if self.all_msg[page][2][0] is not None:
            self.request_header_text.setText(self.all_msg[page][2][0])
        if self.all_msg[page][3][0] is not None:
            self.request_data_text.setText(self.all_msg[page][3][0])
        if self.all_msg[page][4][0] is not None:
            self.response_header_text.setText(self.all_msg[page][4][0])
        if self.all_msg[page][5][0] is not None:
            self.response_data_text.setText(self.all_msg[page][5][0])

        self.url_combo.setCurrentIndex(int(self.all_msg[page][1][1]))
        self.request_header_combo.setCurrentIndex(int(self.all_msg[page][2][1]))
        self.request_data_combo.setCurrentIndex(int(self.all_msg[page][3][1]))
        self.response_header_combo.setCurrentIndex(int(self.all_msg[page][4][1]))
        self.response_data_combo.setCurrentIndex(int(self.all_msg[page][5][1]))

    def page_change(self):
        pass

    def read_msg(self):
        msg = (
            (self.ip_list[0], self.port_list[0]),
            (self.url_list[0], self.url_comb[0]),
            (self.rhe_list[0], self.rhe_comb[0]),
            (self.rda_list[0], self.rda_comb[0]),
            (self.she_list[0], self.she_comb[0]),
            (self.sda_list[0], self.sda_comb[0]),
            self.code_list[0]
        )
        return msg

    def clear_control(self):
        self.code_text.clear()
        self.ip_text.clear(), self.port_text.clear()
        self.url_text.clear(), self.url_combo.setCurrentIndex(0)
        self.request_header_text.clear(), self.request_header_combo.setCurrentIndex(0)
        self.request_data_text.clear(), self.request_data_combo.setCurrentIndex(0)
        self.response_header_text.clear(), self.response_header_combo.setCurrentIndex(0)
        self.response_data_text.clear(), self.response_data_combo.setCurrentIndex(0)
