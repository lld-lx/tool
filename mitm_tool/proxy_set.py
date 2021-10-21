import winreg
import ctypes

# 如果从来没有开过代理 有可能健不存在 会报错
INTERNET_SETTINGS = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    0, winreg.KEY_ALL_ACCESS
)

# 设置刷新
INTERNET_OPTION_REFRESH = 37
INTERNET_OPTION_SETTINGS_CHANGED = 39
internet_set_option = ctypes.windll.Wininet.InternetSetOptionW


def set_key(name, value):   # 修改键值
    reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
    print(reg_type)
    winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type[1], value)


def proxy_start(ip, port):
    # 启用代理
    set_key('ProxyEnable', 1)  # 启用
    set_key('ProxyOverride', u'*.local;<local>')  # 绕过本地
    set_key('ProxyServer', u'%s:%s' % (ip, port))  # 代理IP及端口
    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)


def proxy_shutdown():
    # 停用代理
    set_key('ProxyEnable', 0)  # 停用
    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)


if __name__ == "__main__":
    # proxy_start('127.0.0.1', 8088)
    proxy_shutdown()
