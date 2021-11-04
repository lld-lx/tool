"""记录键盘事件,托管到后台，可以选择时间段来回放操作"""
from ctypes import pointer, POINTER
from record_tool.logger import Logger
from record_tool.record_main import Que
from record_tool.message import SetKbStruct, INPUT

#  low-level keyboard input events
WH_KEYBOARD_LL = 13


def my_func(wParam, lParam):
    lp = lParam.contents
    kb = SetKbStruct(vkCode=lp.vkCode, scanCode=lp.scanCode,
                     flags=lp.flags, time=lp.time, dwExtraInfo=lp.dwExtraInfo)

    st = pointer(INPUT(wParam=wParam, k=pointer(kb)))
    Que.put(st)


def start_keyboard_listen():
    logger = Logger(WH_KEYBOARD_LL, my_func)
    address = logger.get_board_fptr(logger.hook_proc)

    if logger.install_hook_proc(address):
        print("installed keyLogger")

    logger.start_key_log()


if __name__ == "__main__":
    start_keyboard_listen()
