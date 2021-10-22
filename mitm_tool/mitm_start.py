from mitmproxy.options import Options
from mitmproxy.proxy import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent
import threading
import asyncio
from json import loads, dumps


class Addon(object):
    def __init__(self):
        self.num = 1

    @concurrent
    def request(self, flow):
        if flow.request.text:
            try:
                dict_msg = loads(flow.request.text)
                if dict_msg.__contains__("num"):
                    dict_msg["num"] = 2
                    flow.request.text = dumps(dict_msg)
            except:
                pass

    @concurrent
    def response(self, flow):
        self.num = self.num + 1


# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)  # This is the key.
    m.run_loop(loop.run_forever)


# addon: list
def mitmproxy_config(ip, port, addons):
    options = Options(listen_host=ip, listen_port=port, http2=True)
    m = DumpMaster(options, with_termlog=False, with_dumper=False)
    config = ProxyConfig(options)
    m.server = ProxyServer(config)
    for addon in addons:
        m.addons.add(addon)
    return m


def mitmproxy_start(mt):
    # run mitmproxy in backgroud, especially integrated with other server
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop, mt))
    t.start()
    print("----------start------------")
    # Other servers might be started too.
    # print('going to shutdown mitmproxy')


def mitmproxy_shutdown(mt):
    mt.shutdown()


if __name__ == "__main__":
    mitmproxy_s = mitmproxy_config('127.0.0.1', 8088, [Addon()])
    mitmproxy_start(mitmproxy_s)
