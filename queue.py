#encoding=utf-8
import threading
import time
from Queue import Queue

class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            if queue.qsize() > 1000:
                pass
            else:
                count = count +1
                msg = '生成产品'+str(count)
                queue.put(msg)
                print msg
                time.sleep(1)


def do_job():
    print "test"

class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize() < 100:
                pass
            else:
                do_job()
            time.sleep(1)

queue = Queue()


def test():
    #for i in range(500):
    #    queue.put('初始产品'+str(i))
    for i in range(2):
        p = Producer()
        p.start()
    for i in range(5):
        c = Consumer()
        c.start()
if __name__ == '__main__':
    test()