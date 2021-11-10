"""通过传入的参数,构建mitmproxy启动需要的addon类"""
import mitmproxy.http
from mitmproxy import ctx, http
from re import compile, sub
from json import dumps, loads
from mitmproxy.script import concurrent


class HTTP(object):
    """
    @parm:self.url   必填，进行过滤匹配
    @parm:self.code  使用参数时,url需填写host，非2xx直接不发送请求
    以下参数逻辑：为0则使用字典, 为1则完全替换, 为2则使用正则
    @parm:self.requests_headers
    @parm:self.requests_data
    @parm:self.response_headers
    @parm:self.response_data
    """
    def __init__(self, page):
        self.url, \
            self.requests_headers, \
            self.requests_data, \
            self.response_headers, \
            self.response_data, \
            self.code, \
            = (i for i in page)
        self.url_flag = self.url[2]

    @concurrent
    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        if self.code != '':
            if self.url_flag:
                if self.re_compile(flow.request.host, self.url[1]):
                    flow.response = http.HTTPResponse.make(int(self.code))
            else:
                if flow.request.host == self.url[1]:
                    flow.response = http.HTTPResponse.make(int(self.code))
                else:
                    return
        else:
            return

    @concurrent
    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if self.requests_headers[1] == "":
            return
        elif self.requests_headers[0] == "" and self.requests_headers[2] != 1:
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

    @concurrent
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if self.requests_data[1] == "":
            return
        elif self.requests_data[0] == "" and self.requests_data[2] != 1:
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

    @concurrent
    def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
        if self.response_headers[1] == "":
            return
        elif self.response_headers[0] == "" and self.response_headers[2] != 1:
            return
        else:
            for split_value in self.response_headers[0].split(";"):
                flow.response.headers = self.header_func(
                    flow.request.url,
                    flow.response.headers,
                    split_value,
                    self.response_headers[1],
                    self.response_headers[2],
                )

    @concurrent
    def response(self, flow: mitmproxy.http.HTTPFlow):
        if self.response_data[1] == "":
            return
        elif self.response_data[0] == "" and self.response_data[2] != 1:
            return
        else:
            for split_value in self.response_data[0].split(";"):
                flow.response.text = self.data_func(
                    flow.request.url,
                    flow.response.text,
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
            if "[" in item:  # 兼容路径字符串里面  /log/[2]/disk中 [2]取列表
                item = eval(item)[0]
            dictionary = dictionary[item]
        return dictionary

    # 修改字典输入路径的值
    def path_set(self, dictionary, path, set_item):
        path = path.split("/")
        key = path[-1]
        dictionary = self.path_get(dictionary, "/".join(path[:-1]))
        dictionary[key] = set_item

    @staticmethod
    def re_sub(rule, repl, string):
        result = sub(rule, repl, string)
        if result:
            return result
        else:
            return None

    def header_func(self, flow_url, flow_header, compile_key, compile_value, rule):
        if rule == 0:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[1]):
                    self.path_set(flow_header, compile_key, compile_value)
            else:
                if flow_url == self.url[1]:
                    self.path_set(flow_header, compile_key, compile_value)
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
                    self.path_set(read_dict, compile_key, compile_value)
                    return dumps(read_dict)
            # 处理失败则直接返回None
            except Exception as ex:
                print("无法替换成功: %s" % ex)

        if rule == 0:
            if self.url_flag:
                if self.re_compile(flow_url, self.url[1]):
                    change = func(flow_msg)
                else:
                    change = flow_msg
            else:
                if flow_url == self.url[1]:
                    change = func(flow_msg)
                else:
                    change = flow_msg
            return change

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
