"""通过argv读取来自cmd的参数，暂时不做反向代理部分，因为基本用不到，需要反代可以直接用nginx"""
import mitmproxy.http
from mitmproxy import ctx, http
from re import compile, sub
from json import dumps, loads


class HTTP(object):
    def __init__(self, page):
        # ((url, 0), (requests_headers, 1), (...))
        # 一个page对应一页,每页的全部参数传入HTTP封装成mitmproxy启动需要的addon类
        self.url, \
            self.code,\
            self.requests_headers,\
            self.requests_data, \
            self.response_headers, \
            self.response_data \
            = (i for i in page)
        # 为1则使用正则, 为0则使用完全匹配
        self.url_flag = self.url[1]

    @staticmethod
    def re_compile(flow_parm, parm):
        return compile(parm, flow_parm)

    # 请求时就设置,非2xx直接不发送请求,断开连接
    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        if self.code:
            if self.url_flag:
                if self.re_compile(flow.request.url, self.url[0]):
                    flow.response = http.HTTPResponse.make(self.code)
            else:
                if flow.request.url == self.url[0]:
                    flow.response = http.HTTPResponse.make(self.code)
                else:
                    return
        else:
            return

    # 对表头进行替换  (need_match, replace_msg, 0)
    # 为0则使用字典, 为1则完全替换, 为2则使用正则, 为-1则不需要替换
    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        for one_rule in self.requests_headers:
            flow.request.headers = self.header_func(
                flow.request.url,
                flow.request.headers,
                one_rule[0],
                one_rule[1],
                one_rule[2]
            )

    def requests(self, flow: mitmproxy.http.HTTPFlow):
        for one_rule in self.requests_data:
            flow.response.text = self.data_func(
                flow.request.url,
                flow.request.text,
                one_rule[0],
                one_rule[1],
                one_rule[2]
            )

    def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
        for one_rule in self.response_headers:
            flow.response.headers = self.header_func(
                flow.request.url,
                flow.response.headers,
                one_rule[0],
                one_rule[1],
                one_rule[2]
            )

    def response(self, flow: mitmproxy.http.HTTPFlow):
        for one_rule in self.response_data:
            flow.response.text = self.data_func(
                flow.request.url,
                flow.request.text,
                one_rule[0],
                one_rule[1],
                one_rule[2]
            )

    def http_connect_upstream(self, flow: mitmproxy.http.HTTPFlow):
        pass

    def error(self):
        pass

    # 获取字典路径对象
    @staticmethod
    def path_get(dictionary, path):
        for item in path.split("/"):
            try:
                dictionary = dictionary[item]
            except Exception:
                dictionary = dictionary[int(item)]
        return dictionary

    # 修改字典输入路径的值
    def path_set(self, dictionary, path, set_item):
        path = path.split("/")
        key = path[-1]
        dictionary = self.path_get(dictionary, "/".join(path[:-1]))
        try:
            dictionary[key] = set_item
        except Exception:
            dictionary[int(key)] = set_item

        return dictionary

    @staticmethod
    def re_sub(rule, repl, string):
        result = sub(rule, repl, string)
        if result:
            return result
        else:
            return None

    def header_func(self, flow_url, flow_header, compile_key, compile_value, rule):
        if rule == -1:
            return flow_header
        elif rule == 0:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[0]):
                    flow_header = self.path_set(flow_header, compile_key, compile_value)
            else:
                if flow_url == self.url[0]:
                    flow_header = self.path_set(flow_header, compile_key, compile_value)
            return flow_header

        elif rule == 1:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[0]):
                    try:
                        flow_header = dict(compile_value)
                    except Exception as e:
                        print("无法替换成功: %s" % e)
            else:
                if flow_url == self.url[0]:
                    try:
                        flow_header = dict(compile_value)
                    except Exception as e:
                        print("无法替换成功: %s" % e)
            return flow_header

        elif rule == 2:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[0]):
                    flow_header = self.re_sub(compile_key, compile_value, flow_header)
            else:
                if flow_url == self.url[0]:
                    flow_header = self.re_sub(compile_key, compile_value, flow_header)
            return flow_header

    # 专门为请求前和请求后的data的json类型做字典方式的处理
    def data_func(self, flow_url, flow_msg, compile_key, compile_value, rule):
        def func(msg):
            # 视为json格式
            try:
                read_dict = loads(msg)
                if type(read_dict) == dict:
                    result = self.path_set(read_dict, compile_key, compile_value)
                    msg = dumps(result)
            # 处理失败则直接返回None
            except Exception as ex:
                print("无法替换成功: %s" % ex)
            return msg

        if rule == -1:
            return flow_msg

        elif rule == 0:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[0]):
                    flow_msg = func(flow_msg)
            else:
                if flow_url == self.url[0]:
                    flow_msg = func(flow_msg)
            return flow_msg

        elif rule == 1:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[0]):
                    try:
                        flow_msg = compile_value
                    except Exception as e:
                        print("无法替换成功: %s" % e)

            else:
                if flow_url == self.url[0]:
                    try:
                        flow_msg = compile_value
                    except Exception as e:
                        print("无法替换成功: %s" % e)
            return flow_msg

        elif rule == 2:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[0]):
                    flow_msg = self.re_sub(compile_key, compile_value, flow_msg)
            else:
                if flow_url == self.url[0]:
                    flow_msg = self.re_sub(compile_key, compile_value, flow_msg)
            return flow_msg
