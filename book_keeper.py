import logging
import queue
import threading

from order_container import OrderContainer,BID_TYPE,ASK_TYPE



class BookKeeper:

    name = "test"
    bid_list = []
    thread_handle = ""
    messageq = queue.Queue()
    latest_price = None

    #Sellers will be added to asks list
    asks = []

    #Buyers will be added to bids list
    bids = []

    def clean_containers(self):
        for ask_container in self.asks:
            if ask_container.get_orders().empty() is True:
                self.asks.remove(ask_container)

        for bid_container in self.bids:
            if bid_container.get_orders().empty() is True:
                self.bids.remove(bid_container)

    def process_order(self, order):
        type = order.get_type()
        value = order.get_value()
        amount = order.get_amount()

        new_ask = True
        new_bid = True
        def fcn(a):
            c = a.get_value()
            return c

        if type == ASK_TYPE:
            matched = False
            for i in range(len(self.bids)):
                bid_container = self.bids[i]
                if value <= bid_container.get_value():
                    for item in list(bid_container.get_orders().queue):
                        self.latest_price = bid_container.get_value()
                        if amount <= item.get_amount():
                            item.set_amount(item.get_amount() - amount)
                            amount = 0
                            break
                        else:
                            amount = amount - item.get_amount()
                            item.set_amount(0)
                            order.set_amount(amount)
                            bid_container.get_next_order()
                            # if bid_container.get_orders().empty() is True:
                            #     self.bids.remove(bid_container)
                    if amount == 0:
                        matched = True
                        break

            if matched is False:
                # find the container
                for ask_container in self.asks:
                    if value == ask_container.get_value():
                        ask_container.add_new_order(order)
                        new_ask = False
                        break
                if new_ask == True:
                    new_container = OrderContainer(type=ASK_TYPE, value=value)
                    new_container.add_new_order(order)
                    self.asks.append(new_container)

            self.asks = sorted(self.asks, key=fcn, reverse=True)

        if type == BID_TYPE:
            matched = False
            for i in range(len(self.asks)):
                ask_container = list(reversed(self.asks))[i]
                if value >= ask_container.get_value():
                    for item in list(ask_container.get_orders().queue):
                        self.latest_price = ask_container.get_value()
                        if amount <= item.get_amount():
                            item.set_amount(item.get_amount() - amount)
                            amount = 0
                            break
                        else:
                            amount = amount - item.get_amount()
                            item.set_amount(0)
                            order.set_amount(amount)
                            ask_container.get_next_order()
                            # if ask_container.get_orders().empty() is True:
                            #     self.asks.remove(ask_container)

                    if amount == 0:
                        matched = True
                        break

            if matched is False:
                # find the container
                for bid_container in self.bids:
                    if value == bid_container.get_value():
                        bid_container.add_new_order(order)
                        new_bid = False
                        break
                if new_bid == True:
                    new_container = OrderContainer(type=BID_TYPE, value=value)
                    new_container.add_new_order(order)
                    self.bids.append(new_container)

            self.bids = sorted(self.bids, key=fcn, reverse=True)

        # self.clean_containers()

    def keeper_thread_function(self,name):
        logging.info("BookKeeper for [%s] started", name)
        while True:
            order_message = self.messageq.get()

            logging.info("[New order] Type: %s  Value: %0.2f  Amount: %d", order_message.get_type_str()
                         , order_message.get_value()
                         , order_message.get_amount())

            self.process_order(order_message)

            for ask in self.asks:
                amnt_str = ""
                for item in list(ask.get_orders().queue):
                    amnt_str += "%d |" % (item.get_amount())

                if amnt_str is not "":
                    logging.info("[Ask] [%0.2f] - %s",ask.get_value(),amnt_str)

            if self.latest_price is not None:
                logging.info("---------------------------------------------------[Latest Price] [%0.2f]", self.latest_price)

            for bid in self.bids:
                amnt_str = ""
                for item in list(bid.get_orders().queue):
                    amnt_str += "%d |" % (item.get_amount())
                if amnt_str is not "":
                    logging.info("[Bid] [%0.2f] - %s",bid.get_value(),amnt_str)




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

