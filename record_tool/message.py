"""create some structure for python"""
from ctypes import Structure, c_long, c_ulong, c_int


class SetMsStruct(Structure):
    """
    Contains information about
        a simulated mouse event
    """
    _fields_ = [
        ("dx", c_long),
        ("dy", c_long),
        ("mouseData", c_ulong),
        ("dwFlags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", c_long)
    ]


class POINT(Structure):
    """
    The x- and y-coordinates
        of the cursor
    """
    _fields_ = [("x", c_int),
                ("y", c_int)
                ]


class GetMsStruct(Structure):
    """
    Contains information about
        a low-level mouse input event
    """
    _fields_ = [
        ("pt", POINT),
        ("mouseData", c_ulong),
        ("dwFlags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", c_long)
    ]


class GetKbStruct(Structure):
    """
    Contains information about
        a low-level keyboard input even
    """
    _fields_ = [
        ("vkCode", c_ulong),
        ("scanCode", c_ulong),
        ("flags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", c_long)
    ]
