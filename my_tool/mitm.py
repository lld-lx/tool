"""自动启动一个mitmproxy程序，简化代码工作"""
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from qt_members.tool_bar import ToolMember
from PyQt5.QtWidgets import QPushButton, QWidget, QTextEdit, QToolButton
from css.reader import CommonHelper
from mitm_tool.proxy_set import proxy_start
from mitm_tool.create_addon import HTTP
from mitm_tool.mitm_start import mitmproxy_config, mitmproxy_start, mitmproxy_shutdown
from re import sub
from mitm_tool.addons import need_start
import shlex
import subprocess


class MiTm(ToolMember):
    def __init__(self, father, mother):
        super(MiTm, self).__init__(father, mother)
        self.father = father
        self.mother = mother
        self.config = None
        self.qss = CommonHelper().read_qss("./css/tool.qss")

    def tool_bar(self):
        tool_button = self.any_bar(
            'mitmproxy监听', './picture/headers.png',
            "mitm_bar", lambda: self.tool_bar_click()
        )
        return tool_button

    def tool_bar_click(self):
        self.remove()

    # 从面板中读取输入参数
    def start_mitmproxy(self, choose):
        ip = ...
        port = ...
        proxy_start(ip, port)  # 启动代理
        # 从面板输入中读取相关配置信息,每页为一组
        page = ...
        addons = ...

        self.config = mitmproxy_config(ip, port, addons)
        mitmproxy_start(self.config)

        get_url = ...
        set_url = ...
        set_requests_headers = ...

        set_requests_data = ...
        set_response_headers = ...
        set_response_data = ...

    def end_mitmproxy(self):
        mitmproxy_shutdown(self.config)

    def requests_data_callback(self):
        pass

    def response_headers_callback(self):
        pass

    def response_data_callback(self):
        pass

