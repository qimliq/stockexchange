import logging
import queue
import threading
from book_keeper import BookKeeper


class Exchange:

    name = "TestExchange"
    assets = []
    thread_handle = ""
    messageq = queue.Queue()
    latest_price = None


    def process_order(self, order):
        return 0

    def exchange_thread_function(self,name):
        while True:
            order_message = self.messageq.get()

            logging.info("[New order] Type: %s  Value: %0.2f  Amount: %d", order_message.get_type_str()
                         , order_message.get_value()
                         , order_message.get_amount())

            self.process_order(order_message)

    def __init__(self,
                 nm,
                 asset_names):
        for asset in asset_names:
            keeper = BookKeeper(nm=asset['name'])
            self.assets.append(keeper)

        self.name = nm
        self.thread_handle = threading.Thread(target=self.exchange_thread_function, args=(nm,))
        self.thread_handle.start()

    def __del__(self):
        self.name = ""

    def get_name(self):
        return self.name

    def send_message(self, message):
        self.messageq.put(message)

