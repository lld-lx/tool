"""全局"""
from async_http.http import post
from asyncio import get_event_loop, ensure_future
from js2py import EvalJs
from aiofiles import open as opens

context = EvalJs()


class BaiDuTranslater(object):
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
        # js逆向获取sign的值
        # 读取js文件
        async with opens(r"../js/translation.js", "r", encoding="utf-8") as f:
            # 添加至上下文
            context.execute(await f.read())
        # 调用js中的函数生成sign
        sign = context.e(self.query)
        # 将sign加入到data中
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
        loop = get_event_loop()
        task = ensure_future(self.get_content())
        loop.run_until_complete(task)
        content = task.result()
        print(content["trans_result"]["data"][0]["dst"])


if __name__ == '__main__':
    query = input("请输入您要翻译的内容:")
    translater = BaiDuTranslater(query)
    translater.run()
