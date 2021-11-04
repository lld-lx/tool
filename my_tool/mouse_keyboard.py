from threading import Thread
from record_tool.record_main import listen_center
from record_tool.record_mouse import start_mouse_listen
Thread(target=listen_center).start()
Thread(target=start_mouse_listen).start()
