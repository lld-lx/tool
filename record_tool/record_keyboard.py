"""记录键盘事件,托管到后台，可以选择时间段来回放操作"""
from ctypes import windll
from record_tool.logger import Logger


# 使用windll声明user32类型的变量,底下有相关的函数
user32 = windll.user32

#  low-level keyboard input events
WH_KEYBOARD_LL = 13


def my_func(wParam, lParam):
    print(lParam.contents.vkCode)
    print(lParam.contents.scanCode)
    print(lParam.contents.flags)
    print(lParam.contents.time)
    print(lParam.contents.dwExtraInfo)


def start_keyboard_listen():
    logger = Logger(WH_KEYBOARD_LL, my_func)
    address = logger.get_board_fptr(logger.hook_proc)

    if logger.install_hook_proc(address):
        print("installed keyLogger")

    logger.start_key_log()


if __name__ == "__main__":
    start_keyboard_listen()
