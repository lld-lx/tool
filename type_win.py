"""用来顶部工具栏的状态恢复设置，通过记录前个对象，并在新对象进入时，恢复前对象的qss常态样式，同时改变新对象的激活样式实现"""
import math

result = 0  # 定义一个变量
num = 0  # 定义一个变量

# while循环,意思是每次内部的东西从上往下执行完,
# 就回到入口while,检查后面的条件是否满足,不满足则退出
# 这里是True,所以每次检查都不会退出循环,也就是一个死循环(程序止步于此不会再运行循环外的代码了)
while True:
    if num == 59:  # if语句,判断num 等于 59时,满足条件就print()
        print(result)
    elif num == 999:    # if...elif..用来判断更多的信息
        print(result)
    elif num == 9999:
        print(result)
    elif num == 99999:
        print(result)
    elif num == 999999:
        print(result)
        break   # 为了防止死循环一直运行,最后卡死电脑.当程序运行到break就会听话退出循环
    result = result + 1 / (2 * num + 1)  # 做累加, 新的result＝旧result + xxx
    num = num + 1   # 每次循环都加把num加1,用来给上面做计算
