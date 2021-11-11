"""全局"""

from PyQt5.QtWidgets import QDialog, qApp, QAction
from win32clipboard import OpenClipboard, GetClipboardData, CloseClipboard
from PyQt5.QtCore import Qt
from win32con import CF_UNICODETEXT
from async_http.http import post
from asyncio import ensure_future, set_event_loop, new_event_loop
from threading import Thread
from record_tool.get_mouse_position import get_position
from record_tool.record_keyboard import start_keyboard_listen, Que
from pykeyboard import PyKeyboard
from js2py import EvalJs
from time import sleep
from aiofiles import open as opens

context = EvalJs()


class DiyWindow(QDialog):
    def __init__(self, father, send):
        super(DiyWindow, self).__init__()
        self.father = father
        self.send = send
        father.setContextMenuPolicy(Qt.ActionsContextMenu)
        quit_action = QAction("Quit", father)
        quit_action.triggered.connect(qApp.quit)
        tran_action = QAction("划词", father)
        tran_action.triggered.connect(lambda: self._translate())
        father.addAction(quit_action)
        father.addAction(tran_action)
        self.clicked = 0

    def _translate(self):
        self.key = PyKeyboard()
        Thread(target=start_keyboard_listen).start()    # 监听键盘事件
        Thread(target=self.listen_click_translate).start()

    def listen_click_translate(self):
        while True:
            msg = Que.get()
            if msg.contents.k.contents.vkCode == 162 and msg.contents.k.contents.flags == 0:
                self.clicked += 1
            elif msg.contents.k.contents.vkCode != 162:
                self.clicked = 0
            if self.clicked == 2:
                self.clicked = 0
                self.key.press_key(self.key.control_key)
                self.key.press_key("c")
                self.key.release_key(self.key.control_key)
                self.key.release_key("c")
                x, y = get_position()
                Thread(target=self.creat_tip, args=(x, y)).start()
                sleep(0.1)  # 不等待会立即拷贝,可以考虑系统剪切板
                self.show_content()
            else:
                continue

    def show_content(self):
        content = get_text()
        translate = BaiDuTranslate(content)
        translate.run()

    def creat_tip(self, x, y):
        self.send.run(x, y)


class BaiDuTranslate(object):
    """
    百度翻译爬虫
    """

    def __init__(self, query):
        # 初始化
        self.url = "https://fanyi.baidu.com/v2transapi?from=zh&to=en"
        self.query = query
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)"
                          " AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Referer": "https://fanyi.baidu.com/",
            "Cookie": "BAIDUID=714BFAAF02DA927F583935C7A354949A:FG=1;"
                      " BIDUPSID=714BFAAF02DA927F583935C7A354949A;"
                      " PSTM=1553390486; delPer=0;"
                      " PSINO=5; H_PS_PSSID=28742_1463_21125_18559_28723_28557_28697_28585_28640_28604_28626_22160;"
                      " locale=zh; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%"
                      "2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D;"
                      " to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value"
                      "%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1;"
                      " FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1;"
                      " Hm_lvt_afd111fa62852d1f37001d1f980b6800=1553658863,1553766321,1553769980,1553770442;"
                      " Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1553770442;"
                      " Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1553766258,1553766321,1553769980,1553770442;"
                      " Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1553770442"
        }

    async def make_sign(self):
        # 读取js文件
        async with opens(r"./js/translation.js", "r", encoding="utf-8") as f:
            context.execute(await f.read())
        # 调用js中的函数生成sign
        sign = context.e(self.query)
        return sign

    async def make_data(self, lang, sign):
        if lang == "zh":
            to = "en"
        else:
            to = "zh"
        data = {
            "query": self.query,
            "from": lang,
            "to": to,
            "token": "6f5c83b84d69ad3633abdf18abcb030d",
            "sign": sign
        }
        return data

    async def get_content(self):
        sign = await self.make_sign()
        k = await self.now_language()
        data = await self.make_data(k, sign)
        # 发送请求获取响应
        response = await post(
            url=self.url,
            headers=self.headers,
            data=data
        )
        return response

    async def now_language(self):
        url = "https://fanyi.baidu.com/langdetect"
        language = {"query": self.query}
        result = await post(url=url, data=language)
        if not result["error"]:
            return result["lan"]
        else:
            return "en"

    def run(self):
        """运行程序"""
        # 获取翻译内容
        loop = new_event_loop()
        set_event_loop(loop)
        task = ensure_future(self.get_content())
        loop.run_until_complete(task)
        content = task.result()
        print(content["trans_result"]["data"][0]["dst"])


class TipWindow(QDialog):
    def __init__(self, x, y):
        super().__init__()
        self.move(x, y)
        self.resize(70, 25)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowOpacity(0.8)


def get_text():
    OpenClipboard()
    d = GetClipboardData(CF_UNICODETEXT)  # 指定编码为unicode，复制粘贴时中文不会会出现乱码
    CloseClipboard()
    return d


if __name__ == '__main__':
    print(get_text())
    _query = input("请输入您要翻译的内容:")
    _translate = BaiDuTranslate(_query)
    _translate.run()
