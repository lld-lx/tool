from mitmproxy.options import Options
from mitmproxy.proxy import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from os import popen
import threading
import asyncio
import time


class Addon(object):
    def __init__(self):
        self.num = 1

    def request(self, flow):
        flow.request.headers["count"] = str(self.num)

    def response(self, flow):
        self.num = self.num + 1
        flow.response.headers["count"] = str(self.num)
        print(self.num)


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
