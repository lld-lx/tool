"""记录键盘事件,托管到后台，可以选择时间段来回放操作"""
from ctypes import windll
from record_tool.logger import Logger


# 使用windll声明user32类型的变量,底下有相关的函数
user32 = windll.user32

#  low-level keyboard input events
WH_KEYBOARD_LL = 13


def my_func(wParam, lParam):
    print(lParam.contents)


keyLogger = Logger(WH_KEYBOARD_LL, my_func)
address = keyLogger.get_fptr(keyLogger.hook_proc)

if keyLogger.install_hook_proc(address):
    print("installed keyLogger")

keyLogger.start_key_log()
