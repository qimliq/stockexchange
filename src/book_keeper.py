import threading
import logging
import time
import queue
from src.order_container import OrderContainer,BID_TYPE,ASK_TYPE
from src.order import Order

class BookKeeper:

    name = "test"
    bid_list = []
    thread_handle = ""
    messageq = queue.Queue()

    #Sellers will be added to asks list
    asks = []

    #Buyers will be added to bids list
    bids = []


    def keeper_thread_function(self,name):
        while True:
            order_message = self.messageq.get()
            type = order_message.get_type()
            value = order_message.get_value()
            amount = order_message.get_amount()
            new_ask = True
            new_bid = True

            if type == ASK_TYPE:
                #find the container
                for ask_container in self.asks:
                    if value == ask_container.get_value():
                        ask_container.add_order(order_message)
                        new_ask = False
                        break
                if new_ask == True:
                    new_container = OrderContainer(type=ASK_TYPE, value= value)
                    new_container.add_order(order_message)
                    self.asks.append(new_container)

            if type == BID_TYPE:
                # find the container
                for bid_container in self.bids:
                    if value == bid_container.get_value():
                        bid_container.add_order(order_message)
                        new_bid = False
                        break
                if new_bid == True:
                    new_container = OrderContainer(type=BID_TYPE, value=value)
                    new_container.add_order(order_message)
                    self.bids.append(new_container)

            logging.debug("[New order] Type: %d  Value: %0.2f  Amount: %d", order_message.get_type()
                         , order_message.get_value()
                         , order_message.get_amount())

            for ask in self.asks:
                logging.info("[Ask] [%0.2f]",ask.get_value())

            for bid in self.bids:
                logging.info("[Bid] [%0.2f]",bid.get_value())




    def __init__(self,
                 nm):
        self.name = nm
        self.thread_handle = threading.Thread(target=self.keeper_thread_function, args=(nm,))
        self.thread_handle.start()

    def __del__(self):
        self.name = ""

    def get_name(self):
        return self.name

    def send_message(self, message):
        self.messageq.put(message)

