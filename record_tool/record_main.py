"""监听队列中的消息，将消息存入数据库中, 与监听部分独立(非同线程)
   保留部分疑问,双线程应该有可能导致小范围的鼠标、键盘顺序出错，但是
   考虑到实际同时切换，严格要求顺序正确的场景很少，所以有问题了再考虑优化"""
from ctypes import CDLL, POINTER
from queue import Queue
from record_tool.message import INPUT
Que = Queue()


def listen_center():
    num = 0
    insert = CDLL("../dlls/set_sqlite.dll", winmode=0)
    struct = (POINTER(INPUT) * 10)()
    insert.create_database(bytes("../sqlite/MKEvent.db", encoding='utf-8'))  # 创建连接，db获取句柄
    while True:
        st = Que.get()
        if st:
            struct[num] = st
            num += 1
            if num == 10:
                insert.insert_database(struct)
                num = 0


if __name__ == "__main__":
    from threading import Thread

    def add_msg():
        for i in range(10):
            Que.put(INPUT())

    Thread(target=listen_center).start()
    Thread(target=add_msg).start()
