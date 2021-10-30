from ctypes import windll, CFUNCTYPE, c_int, POINTER, c_void_p, byref
from ctypes.wintypes import MSG

dwThreadId = 0


# 定义类：定义拥有挂钩与拆钩功能的类
class Logger:
    def __init__(self, id_type, my_func):
        self.mod = windll.kernel32.GetModuleHandleW
        self.close = windll.user32.UnhookWindowsHookEx
        self.hooked = None
        self.my_func = my_func
        self.id_type = id_type

    # 定义挂钩函数：使用user32DLL的SetWindowsHookExA函数设置钩子。
    # 构造结构可参考微软公开的dll文档
    def install_hook_proc(self, lpfn):
        self.hooked = windll.user32.SetWindowsHookExA(
            self.id_type,
            lpfn,
            self.mod(None),
            dwThreadId
        )
        if not self.hooked:
            return False
        return True

    # 定义拆钩函数：调用user32Dll的SetWindowsHookEx()函数，拆除之前设置的钩子。
    def uninstall_hook_proc(self):
        if self.hooked is None:
            return
        self.close(self.hooked)
        self.hooked = None

    # 获取函数指针：若想注册钩子过程(回调函数)，必须传入函数指针。ctypes为此提供了专门的方法。
    # 通过CFUNCTYPE()创建并返回使用标准C调用约定的函数, 参数参考CFUNCTYPE自带说明
    @staticmethod
    def get_fptr(fn):
        creat_func = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        return creat_func(fn)

    # 传递消息：GetMessageA()函数函数监视队列，消息进入队列后取出消息，并传递给勾连中的第一个钩子
    @staticmethod
    def start_key_log():
        msg = MSG()
        windll.user32.GetMessageA(byref(msg), 0, 0, 0)

    def hook_proc(self, nCode, wParam, lParam):
        """
            nCode: If nCode is less than zero, the hook procedure must pass the message to the CallNextHookEx
                function without further processing and should return the value returned by CallNextHookEx.
        """
        if nCode >= 0:
            self.my_func(wParam, lParam)
        return windll.user32.CallNextHookEx(self.hooked, nCode, wParam, lParam)