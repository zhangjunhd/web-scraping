import time
import threading
import copy
from rw_lock import RWLock


class NormalQueue(object):
    def __init__(self, item_list):
        self.work = item_list
        self.rest = []

    def get_work(self):
        return self.work

    def get_rest(self):
        return self.rest


class ShiftQueue(threading.Thread):
    def __init__(self, item_list, shift_sec=1):
        super(ShiftQueue, self).__init__()
        if len(item_list) <= 1:
            self.work = item_list
            self.rest = item_list
        else:
            self.work = item_list[:len(item_list)/2]
            self.rest = item_list[len(item_list)/2:]
        self.shift_sec = shift_sec
        self.rwl = RWLock()

    def run(self):
        self._shift(self.shift_sec)

    def get_work(self):
        self.rwl.acquire_read()
        temp = copy.deepcopy(self.work)
        self.rwl.release()
        return temp

    def get_rest(self):
        self.rwl.acquire_read()
        temp = copy.deepcopy(self.rest)
        self.rwl.release()
        return temp

    def _shift(self, sec):
        while True:
            time.sleep(sec)
            self.rwl.acquire_write()
            temp = self.work
            self.work = self.rest
            self.rest = temp
            self.rwl.release()

if __name__ == "__main__":
    shift_queue = ShiftQueue([1])
    shift_queue.start()
    for i in range(100):
        print '[%d]work:%s,rest:%s' % (i, str(shift_queue.get_work()), str(shift_queue.get_rest()))
        time.sleep(0.5)
