"""通过传入的参数,构建mitmproxy启动需要的addon类"""
import mitmproxy.http
from mitmproxy import ctx, http
from re import compile, sub
from json import dumps, loads
from mitmproxy.script import concurrent


class HTTP(object):
    def __init__(self, page):
        self.url, \
            self.requests_headers, \
            self.requests_data, \
            self.response_headers, \
            self.response_data, \
            self.code, \
            = (i for i in page)
        self.url_flag = self.url[2]

    # 请求时就设置,非2xx直接不发送请求,断开连接
    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        print("http_connect")
        if self.code != '':
            if self.url_flag:
                if self.re_compile(flow.request.url, self.url[1]):
                    flow.response = http.HTTPResponse.make(self.code)
            else:
                if flow.request.url == self.url[1]:
                    flow.response = http.HTTPResponse.make(self.code)
                else:
                    return
        else:
            return

    # 对表头进行替换  (need_match, replace_msg, 0)
    # 为0则使用字典, 为1则完全替换, 为2则使用正则, 为-1则不需要替换
    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        print("RequestHeaders")
        if (self.requests_headers[0] == "") or (self.requests_headers[1] == ""):
            return
        else:
            for split_value in self.requests_headers[0].split(";"):
                flow.request.headers = self.header_func(
                    flow.request.url,
                    flow.request.headers,
                    split_value,
                    self.requests_headers[1],
                    self.requests_headers[2]
                    )

    def request(self, flow: mitmproxy.http.HTTPFlow):
        print("Requests")
        if (self.requests_data[0] == "") or (self.requests_data[1] == ""):
            return
        else:
            for split_value in self.requests_data[0].split(";"):
                flow.request.text = self.data_func(
                    flow.request.url,
                    flow.request.text,
                    split_value,
                    self.requests_data[1],
                    self.requests_data[2],
                )

    def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
        print("responseheaders")
        if (self.response_headers[0] == "") or (self.response_headers[1] == ""):
            return
        else:
            for split_value in self.response_headers[0].split(";"):
                flow.response.headers = self.header_func(
                    flow.request.url,
                    flow.request.text,
                    split_value,
                    self.response_headers[1],
                    self.response_headers[2],
                )

    def response(self, flow: mitmproxy.http.HTTPFlow):
        print("response")
        if (self.response_data[0] == "") or (self.response_data[1] == ""):
            return
        else:
            for split_value in self.response_data[0].split(";"):
                flow.response.text = self.data_func(
                    flow.request.url,
                    flow.request.text,
                    split_value,
                    self.response_data[1],
                    self.response_data[2],
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
        if "/".join(path[:-1]):
            self.path_get(dictionary, "/".join(path[:-1]))
        else:
            dictionary[key] = set_item
            return dictionary

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
                if self.re_compile(flow_url, self.url[1]):
                    flow_header = self.path_set(flow_header, compile_key, compile_value)
            else:
                if flow_url == self.url[1]:
                    flow_header = self.path_set(flow_header, compile_key, compile_value)
            return flow_header
        elif rule == 1:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[1]):
                    try:
                        flow_header = dumps(compile_value)
                    except Exception as e:
                        print("无法替换成功: %s" % e)
            else:
                if flow_url == self.url[1]:
                    try:
                        flow_header = dumps(compile_value)
                    except Exception as e:
                        print("无法替换成功: %s" % e)
            return flow_header

        elif rule == 2:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[1]):
                    flow_header = self.re_sub(compile_key, compile_value, flow_header)
            else:
                if flow_url == self.url[1]:
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
                if self.re_compile(flow_url, self.url[1]):
                    flow_msg = func(flow_msg)
            else:
                if flow_url == self.url[1]:
                    flow_msg = func(flow_msg)
            return flow_msg

        elif rule == 1:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[1]):
                    try:
                        flow_msg = compile_value
                    except Exception as e:
                        print("无法替换成功: %s" % e)

            else:
                if flow_url == self.url[1]:
                    try:
                        flow_msg = compile_value
                    except Exception as e:
                        print("无法替换成功: %s" % e)
            return flow_msg

        elif rule == 2:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[1]):
                    flow_msg = self.re_sub(compile_key, compile_value, flow_msg)
            else:
                if flow_url == self.url[1]:
                    flow_msg = self.re_sub(compile_key, compile_value, flow_msg)
            return flow_msg

    @staticmethod
    def re_compile(flow_parm, parm):
        return compile(parm, flow_parm)

