"""监听队列中的消息，将消息存入数据库中, 与监听部分独立(非同线程)"""
from ctypes import CDLL, POINTER, pointer, byref
from queue import Queue
from record_tool.message import INPUT
Que = Queue()


def listen_center():
    num = 0
    insert = CDLL("../dlls/set_sqlite.dll", winmode=0)
    struct = (POINTER(INPUT) * 10)()
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
