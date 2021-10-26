from mitmproxy import http, ctx
from mitmproxy.options import Options
from mitmproxy.proxy import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
import threading
import asyncio
num = 0


# for example
class Addon(object):
    def __init__(self):
        pass

    @staticmethod
    def http_connect(flow: http.HTTPFlow):
        if flow.request.host == "www.baidu.com":
            flow.response = http.HTTPResponse.make(404)


# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)  # This is the key.
    m.run_loop(loop.run_forever)


# addon: list
def mitmproxy_config(ip, port, addons):
    global num
    if not num:
        loop = asyncio.get_event_loop()
        num += 1
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    options = Options(listen_host=ip, listen_port=port, http2=True)
    m = DumpMaster(options, with_termlog=False, with_dumper=False)
    config = ProxyConfig(options)
    m.server = ProxyServer(config)
    for addon in addons:
        m.addons.add(addon)
    return m, loop


def mitmproxy_start(mt, loop):
    # run mitmproxy in backgroud, especially integrated with other server
    t = threading.Thread(target=loop_in_thread, args=(loop, mt))
    print("loop1: %s" % id(loop))
    t.start()
    print("----------start------------")
    # Other servers might be started too.
    # print('going to shutdown mitmproxy')


def mitmproxy_shutdown(mt):
    mt.shutdown()
    print("----------end------------")


if __name__ == "__main__":
    mitmproxy_s = mitmproxy_config('127.0.0.1', 8088, [Addon()], 0)
    mitmproxy_start(mitmproxy_s, 1)
