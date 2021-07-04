import platform
import ctypes

class multi_os:
    def msg_box(self, msg, title=""): # 提示用户需要自行答题等
        sys = platform.system()
        if sys == "Windows":
            ctypes.windll.user32.MessageBoxW(0, msg, title, 1)
        elif sys == "Linux":
            print("检测到 Linux 系统，没有相关的 multi_os.msg_box 函数")
        else:
            print("检测到 未知 系统，没有相关的 multi_os.msg_box 函数")
