"""记录鼠标事件、位置将记录托管到后台，可以选择时间段来回放操作"""
from ctypes import windll
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
        WM_MOUSEHWHEEL、WM_RBUTTONDOWN或WM_RBUTTONUP.
    lParam: A pointer to an MSLLHOOKSTRUCT structure, some of parameter:
        pt:The x- and y-coordinates of the cursor
        time:The time stamp for this message
    """
    for i in range(5):
        print(lParam[i])


# 启动消息钩取，首先创造KeyLogger 类，然后installHookProc（）函数设置钩子，同时
# 注册钩子过程回调函数。最后调用startKeyLog（）函数，将进入队列的消息传递给勾连
logger = Logger(WH_MOUSE_LL, my_func)
address = logger.get_fptr(logger.hook_proc)

if logger.install_hook_proc(address):
    print("installed keyLogger")

logger.start_key_log()
