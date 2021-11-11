from ctypes import windll, pointer
from record_tool.message import Position
user32 = windll.user32


def get_position():
    msg = pointer(Position())
    result = user32.GetCursorPos(msg)
    if result:
        return msg.contents.dx, msg.contents.dy
    else:
        print("error")

