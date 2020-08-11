from threading import Thread
from threading import Lock

threadLock = Lock()
threads = []


class MyThread(Thread):
    def __init__(self, name, func, *args, lock=False):
        Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.lock = lock

    def run(self):
        print("开启： " + self.name)
        if self.lock:
            threadLock.acquire()
            self.func(*self.args)
            threadLock.release()
        else:
            self.func(*self.args)
