from threading import Thread
from queue import Queue
import time

queue = Queue()


class FResult:
    def __init__(self):
        self.hasresult = False
        self.endresult = None


    def setresult(self, result):
        self.hasresult = True
        self.endresult = result


    def result(self):
        while not self.hasresult:
            time.sleep(1)
        return self.endresult


    def getendresult(self):
        return self.endresult


class Worker:
    def __init__(self, func, arg):
        self.function = func
        self.arg = arg
        self.future = FResult()


class WorkerThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active = True

        global queue


    def end(self):
        self.is_active = False


    def run(self):
        while True:
            if not self.is_active:
                return
            item = queue.get()
            res = item.function(item.arg)
            item.future.setresult(res)


args = range(1, 5)


def function(x):
    time.sleep(5)
    return x


class CExecutor:
    def __init__(self, threadsmax):
        self.sizemax = threadsmax
        self.workers = []
        for _ in range(threadsmax):
            self.workers.append(WorkerThread())
            self.workers[-1].start()


    def shutdown(self):
        for w in self.workers:
            w.end()


    def execute(self, func, arg):
        item = Worker(func, arg)
        queue.put(item)
        return item.future


    def map(self, func, args):
        futures_ = []
        for arg in args:
            futures_.append(self.execute(func, arg))

        return futures_


if __name__ == '__main__':
    executor = CExecutor(threadsmax=2)
    futures = executor.map(func=function, args=args)

    for f in futures:
        print(f.result())

    executor.shutdown()
