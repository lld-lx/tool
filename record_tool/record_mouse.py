"""记录鼠标事件、位置,存入队列后,由中心将数据存入数据库中
这里将数据转了一次后再丢给c去写入数据库，理论上直接存也行
究竟是c去写快还是py直接写快，我觉得优化后应该是c，但是py
中使用异步的手段很方便所以也行正常还是py直接写进数据库快"""
from ctypes import windll, pointer
from record_tool.message import INPUT, SetMsStruct
from record_tool.record_main import Que
from record_tool.logger import Logger


# 使用windll声明user32类型的变量,底下有相关的函数
user32 = windll.user32

# low-level mouse input events
WH_MOUSE_LL = 14


# Hook function, callback the captured mouse information
def my_func(wParam, lParam):
    """
    wParam: The identifier of the mouse message. This parameter can be one of the following messages:
        WM_LBUTTONDOWN、WM_LBUTTONUP、WM_MOUSEMOVE、WM_MOUSEWHEEL、
        WM_MOUSEHWHEEL、WM_RBUTTONDOWN or WM_RBUTTONUP.
    """
    lp = lParam.contents
    ms = SetMsStruct(dx=lp.pt.x, dy=lp.pt.y, mouseData=lp.mouseData,
                     dwFlags=lp.dwFlags, time=lp.time, dwExtraInfo=lp.dwExtraInfo)

    st = INPUT(wParam=wParam, m=pointer(ms))
    Que.put(st)


def start_mouse_listen():
    # 启动消息钩取，首先创造KeyLogger 类，然后installHookProc（）函数设置钩子，同时
    # 注册钩子过程回调函数。最后调用startKeyLog（）函数，将进入队列的消息传递给勾连
    logger = Logger(WH_MOUSE_LL, my_func)
    address = logger.get_mouse_fptr(logger.hook_proc)

    if logger.install_hook_proc(address):
        print("installed mouseLogger")

    logger.start_key_log()


if __name__ == "__main__":
    start_mouse_listen()
