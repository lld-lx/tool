"""将从浏览器复制下来的表头转换为字典格式"""
from PyQt5.QtWidgets import QPushButton, QTextEdit
from qt_members.tool_bar import ToolMember
from re import findall


class BrowserHeaders(ToolMember):
    def __init__(self, father, mother):
        super(BrowserHeaders, self).__init__(father, mother)
        self.textEdit = None
        self.start_button = None
        self.button = self.tool_bar()
        self.add_widget()

    # 读取输入内容，转换为字典后加入文本控件中
    def format_conversion(self):
        headers = self.textEdit.toPlainText() + "\n"
        result = findall("(.*[ \n].*)?\n", headers)
        if result != ['']:
            self.textEdit.clear()
            self.textEdit.append("{")
            try:
                for i in result:
                    format_list = i.split(": \n")
                    key = format_list[0]
                    value = format_list[1]
                    if "'" in key and "'" in value:
                        self.textEdit.append(
                            '<font color=\"#BB0F06\" face="微软雅黑" size="3">&nbsp;&nbsp;&nbsp;&nbsp;"%s": </font>' % key +
                            '<font color=\"#09F001\" face="微软雅黑" size="2">"%s",</font>' % value +
                            '\n'
                        )
                    elif '"' in key and "'" in value:
                        self.textEdit.append(
                            """<font color=\"#BB0F06\" face="微软雅黑" size="3">&nbsp;&nbsp;&nbsp;&nbsp;'%s': </font>""" % key +
                            '<font color=\"#09F001\" face="微软雅黑" size="2">"%s",</font>' % value +
                            '\n'
                        )
                    elif "'" in key and '"' in value:
                        self.textEdit.append(
                            '<font color=\"#BB0F06\" face="微软雅黑" size="3">&nbsp;&nbsp;&nbsp;&nbsp;"%s": </font>' % key +
                            """<font color=\"#09F001\" face="微软雅黑" size="2">'%s',</font>""" % value +
                            '\n'
                        )
                    else:
                        self.textEdit.append(
                            """<font color=\"#BB0F06\" face="微软雅黑" size="3">&nbsp;&nbsp;&nbsp;&nbsp;'%s': </font>""" % key +
                            """<font color=\"#09F001\" face="微软雅黑" size="2">'%s',</font>""" % value +
                            '\n'
                        )
                self.textEdit.append("}")
            except Exception as e:
                print(e)
        else:
            pass

    # 调用父类方法创建一个QToolButton
    def tool_bar(self):
        tool_button = self.any_bar(
            '浏览器表头转换', './picture/headers.png',
            "headers_bar", lambda: self.tool_bar_click()
        )
        return tool_button

    @staticmethod
    def tool_body():
        body = QTextEdit()
        body.setObjectName("headers_body")
        return body

    def tool_under_button(self):
        start_button = QPushButton()
        start_button.clicked.connect(lambda: self.format_conversion())
        return start_button

    def add_widget(self):
        self.father.addWidget(self.button)

    def tool_bar_click(self):
        self.remove()
        self.textEdit = self.tool_body()
        start_button = self.tool_under_button()
        self.textEdit.setStyleSheet(self.qss)
        self.mother.addWidget(self.textEdit)
        self.mother.addWidget(start_button)
