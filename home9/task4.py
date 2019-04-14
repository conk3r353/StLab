from threading import Thread, Lock, BoundedSemaphore, Condition, Event, Barrier, BrokenBarrierError
from time import sleep


class ClientThread(Thread):
    def __init__(self, number, lock):
        Thread.__init__(self)
        self.number = number
        self.lock = lock

    def run(self):
        print(self.number)
        sleep(2)
        self.lock.release()


class ClientThread2(Thread):
    def __init__(self, number, lock):
        Thread.__init__(self)
        self.number = number
        self.lock = lock

    def run(self):
        print(self.number)
        sleep(self.number * 0.5)
        self.lock.release()


class TouristThread(Thread):
    def __init__(self, number, condition):
        Thread.__init__(self)
        self.number = number
        self.condition = condition

    def run(self):
        with self.condition:
            self.condition.wait()
            print(self.number)


class EventTouristThread(Thread):
    def __init__(self, number, event):
        Thread.__init__(self)
        self.number = number
        self.event = event

    def run(self):
        self.event.wait()
        print(self.number)


class RollerCoasterThread(Thread):
    def __init__(self, number, barrier):
        Thread.__init__(self)
        self.number = number
        self.barrier = barrier

    def run(self):
        try:
            self.barrier.wait()
        except BrokenBarrierError:
            self.barrier.reset()
        print(self.number)


def client():
    lock = Lock()
    for i in range(3):
        lock.acquire()
        thread = ClientThread(i, lock)
        thread.start()


def border_guard(condition):
    count = 0
    while count < 3:
        with condition:
            condition.notify()
        count += 1
        sleep(1)
    sleep(1)
    with condition:
        condition.notify_all()


def tourist():
    condition = Condition()

    for i in range(6):
        tourist_thread = TouristThread(i, condition)
        tourist_thread.start()

    sleep(3)
    Thread(target=border_guard, args=[condition]).start()


def client_2():
    semaphore = BoundedSemaphore(3)
    for i in range(9):
        semaphore.acquire()
        thread = ClientThread2(i, semaphore)
        thread.start()


def border_guard_event(event):
    sleep(4)
    event.set()
    sleep(2)
    event.clear()
    sleep(4)
    event.set()


def tourist_2():
    event = Event()
    event.clear()
    Thread(target=border_guard_event, args=[event]).start()

    for i in range(9):
        tourist_thread = EventTouristThread(i, event)
        tourist_thread.start()
        sleep(1)


def roller_coaster():
    barrier = Barrier(5, timeout=4)

    for i in range(20):
        roller_coaster_thread = RollerCoasterThread(i, barrier)
        roller_coaster_thread.start()
        sleep(0.5)
    for i in range(20, 30):
        roller_coaster_thread = RollerCoasterThread(i, barrier)
        roller_coaster_thread.start()
        sleep(1)
    for i in range(30, 35):
        roller_coaster_thread = RollerCoasterThread(i, barrier)
        roller_coaster_thread.start()
        sleep(2)
