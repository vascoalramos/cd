import random
import uuid
from queue import Queue
from utils import work


class Restaurant():
    def __init__(self):
        self.orders = Queue()
        self.task = Queue()
        self.pending = Queue()
        self.deliver = Queue()

    def add_order(self, order):
        order_id = uuid.uuid1()
        self.orders.put((order_id, order))
        return order_id

    def get_task(self):
        if self.orders.empty():
            return False
        return self.orders.get()

    def add_order_task(self, order):
        self.task.put(order)

    def cook(self):
        if self.task.empty():
            return False
        return self.task.get()

    def add_meal_cooked(self, order):
        self.pending.put(order)

    def get_meal_deliver(self):
        if self.pending.empty():
            return False
        return self.pending.get()

    def add_ready_meal(self, order):
        self.deliver.put(order)

    def pickup(self, order_id):
        if self.deliver.empty() or self.deliver.queue[0][0] != order_id:
            return False
        return self.deliver.get()[0]


class Grelhador:
    def __init__(self,mean,std_deviation):
        self.mean=mean
        self.std_deviation=std_deviation

    def grelhar(self):
        slp_time=random.gauss(mean,pow(std_deviation,2))
        time.sleep(slp_time/1000)

class Dispensador:
    def __init__(self,mean,std_deviation):
        self.mean=mean
        self.std_deviation=std_deviation

    def dispensar(self):
        slp_time=random.gauss(mean,pow(std_deviation,2))
        time.sleep(slp_time/1000)

class Fritadeira:
    def __init__(self,mean,std_deviation):
        self.mean=mean
        self.std_deviation=std_deviation

    def fritar(self):
        slp_time=random.gauss(mean,pow(std_deviation,2))
        time.sleep(slp_time/1000)
