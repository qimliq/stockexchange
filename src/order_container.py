import queue

BID_TYPE = 0
ASK_TYPE = 1

class OrderContainer:
    order_type = BID_TYPE
    order_queue = queue.Queue()
    order_value = 0

    def __init__(self, type, value):
        self.order_type = type
        self.order_value = value

    def get_type(self):
        return self.order_type

    def get_value(self):
        return self.order_value

    def add_order(self,order):
        self.order_queue.put(order)

    def remove_order(self):
        return self.order_queue.get()

    def get_orders(self):
        return self.order_queue