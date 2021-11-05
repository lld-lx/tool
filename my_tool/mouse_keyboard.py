from threading import Thread
from record_tool.record_main import listen_center
from record_tool.record_mouse import start_mouse_listen
from record_tool.record_keyboard import start_keyboard_listen
Thread(target=listen_center).start()
Thread(target=start_mouse_listen).start()
Thread(target=start_keyboard_listen).start()
