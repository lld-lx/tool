"""监听队列中的消息，将消息存入数据库中, 与监听部分独立(非同线程)"""
from queue import Queue
Que = Queue()


def listen_center():
    while True:
        if Que.full():
            ...  # 调用c封装好的dll文件写入数据库
