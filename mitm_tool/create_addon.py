"""通过argv读取来自cmd的参数，暂时不做反向代理部分，因为基本用不到，需要反代可以直接用nginx"""
import mitmproxy.http
from mitmproxy import ctx, http
import json
from sys import argv
from re import compile

replace = argv[1:]


# 所有的入参都是callback,以提供自由的修改
class HTTP(object):
    def __init__(self):
        self.url, \
            self.code,\
            self.requests_headers,\
            self.requests_data, \
            self.response_headers, \
            self.response_data \
            = (i for i in replace)
        # 为True则使用[0]的正则, 为False则使用[0]完全匹配
        self.url_flag = self.url[1]
        # 为0则使用字典, 为1则完全替换, 为2则使用正则, 为-1则不需要替换
        self.requests_headers_flag = self.requests_headers[1]
        self.requests_data_flag = self.requests_data[1]
        self.response_headers_flag = self.response_headers[1]
        self.response_data_flag = self.response_data[1]

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

    # 对表头进行替换
    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        if self.requests_headers_flag == -1:
            return
        elif self.requests_headers_flag == 0:
            if self.url_flag:
                if self.re_compile(flow.request.url, self.url[0]):
                    pass
            else:
                pass
        elif self.requests_headers_flag == 1:
            if self.url_flag:
                if self.re_compile(flow.request.url, self.url[0]):
                    pass
            else:
                pass
        elif self.requests_headers_flag == 2:
            if self.url_flag:
                if self.re_compile(flow.request.url, self.url[0]):
                    pass
            else:
                pass

    def requests(self, flow: mitmproxy.http.HTTPFlow):
        if self.flag == 0:
            if self.requests_data:
                data = self.requests_headers_callback(flow.request.text, self.requests_data[0], self.requests_data[1])
                flow.request.set_text(data)
            else:
                return
        elif self.flag == 1:
            if self.requests_data:
                data = self.requests_headers_callback(flow.request.text, self.requests_data[0], self.requests_data[1])
                flow.request.set_text(data)
            else:
                return
        elif self.flag == 2:
            pass
        else:
            pass

    def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
        pass

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url != self.url:
            return
        response = flow.response.json()
        response = self.response_data(response)
        flow.response.set_text(json.dumps(response))  # 设置请求返回结果

    def http_connect_upstream(self, flow: mitmproxy.http.HTTPFlow):
        pass

    def error(self):
        pass

    @staticmethod
    def url_callback(get_url, set_url):
        if set_url:
            return set_url
        else:
            return get_url

    @staticmethod
    def requests_headers_callback(get_requests_headers, set_requests_headers, *args):
        if set_requests_headers:
            if args == 0:   # 字典格式
                return get_requests_headers + ...
            elif args == 1:  # re模式
                pass
            else:   # 直接替换
                pass
        else:
            return None

# 执行script可以直接不需要下面这段直接 mitmdump –s response_change.py
# 但是另起一个addons.py存放addons，监听的时候直接-s addons.py，会方便管理查看很多
