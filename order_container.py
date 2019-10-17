import queue

from constants import BID_TYPE,ASK_TYPE


class OrderContainer:
    order_type = None
    order_queue = None
    order_value = None

    def __init__(self, type, value):
        self.order_type = type
        self.order_value = value
        self.order_queue = queue.Queue()

    def get_type(self):
        return self.order_type

    def get_value(self):
        return self.order_value

    def add_new_order(self, order):
        self.order_queue.put(order)

    def get_next_order(self):
        return self.order_queue.get()

    def edit_order(self, id, value, amount):
        return 0

    def cancel_order(self, id):
        return 0

    def get_orders(self):
        return self.order_queue