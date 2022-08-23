import time
from threading import Thread, Event

class MyThread1(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        x = 0
        while not self.stopped.wait(0.5):
            if x == 5:
                    thread2.start()
            print("Thread 1 is running..")
            x += 1


class MyThread2(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print("Procces 2 start and the process 1 will stop in 2 seconds")
        x = 0
        while x < 10:
            if x == 5:
                my_event.set()
            print("x = ",x)
            time.sleep(0.5)
            x += 1

my_event = Event()
thread1 = MyThread1(my_event)
thread2 = MyThread2()

thread1.start()