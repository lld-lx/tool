from ctypes import Structure, c_long, c_ulong


class MsStruct(Structure):
    """Contains information about a simulated mouse event"""
    _field_ = [
        ("dx", c_long),
        ("dy", c_long),
        ("mouseData", c_ulong),
        ("dwFlags", c_ulong),
        ("time", c_ulong),
        ("dwExtraInfo", c_long)
    ]
