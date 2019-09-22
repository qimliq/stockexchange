import logging
import queue
import threading

from order_container import OrderContainer
from constants import BID_TYPE, ASK_TYPE


class BookKeeper:

    name = None
    id = None
    exchange = None

    bid_list = []
    thread_handle = ""
    messageq = None
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

    def process_command(self, cmd):

        # investor : type + payload where payload: dict(investor id, order)
        # broker   : type + payload where payload: dict(broker, investor cmd)
        # exchange : broker cmd

        payload = cmd.get_payload()
        subcmd = payload['subcommand']

        subcmd_payload = subcmd.get_payload()

        investor_id = subcmd_payload['investor']
        order = subcmd_payload['order']

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
                    for command in list(bid_container.get_orders().queue):
                        payload = command.get_payload()
                        subcmd = payload['subcommand']
                        subcmd_payload = subcmd.get_payload()

                        item = subcmd_payload['order']

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
                        ask_container.add_new_order(cmd)
                        new_ask = False
                        break
                if new_ask == True:
                    new_container = OrderContainer(type=ASK_TYPE, value=value)
                    new_container.add_new_order(cmd)
                    self.asks.append(new_container)

            self.asks = sorted(self.asks, key=fcn, reverse=True)

        if type == BID_TYPE:
            matched = False
            for i in range(len(self.asks)):
                ask_container = list(reversed(self.asks))[i]
                if value >= ask_container.get_value():
                    for command in list(ask_container.get_orders().queue):
                        payload = command.get_payload()
                        subcmd = payload['subcommand']
                        subcmd_payload = subcmd.get_payload()

                        item = subcmd_payload['order']

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
                        bid_container.add_new_order(cmd)
                        new_bid = False
                        break
                if new_bid == True:
                    new_container = OrderContainer(type=BID_TYPE, value=value)
                    new_container.add_new_order(cmd)
                    self.bids.append(new_container)

            self.bids = sorted(self.bids, key=fcn, reverse=True)

        # self.clean_containers()

    def keeper_thread_function(self,name):
        logging.info("BookKeeper for [%s][id: %d] started", name, self.id)
        while True:
            cmd = self.messageq.get()

            logging.info("[Bookkeeper [%d]][New order] Type: %d ", self.id, cmd.get_type())

            self.process_command(cmd)

            for ask in self.asks:
                amnt_str = ""
                for command in list(ask.get_orders().queue):
                    payload = command.get_payload()
                    subcmd = payload['subcommand']
                    subcmd_payload = subcmd.get_payload()
                    item = subcmd_payload['order']
                    amnt_str += "%d |" % (item.get_amount())

                if amnt_str is not "":
                    logging.info("[Ask] [%0.2f] - %s",ask.get_value(),amnt_str)

            if self.latest_price is not None:
                logging.info("---------------------------------------------------[Latest Price] [%0.2f]", self.latest_price)

            for bid in self.bids:
                amnt_str = ""
                for command in list(bid.get_orders().queue):
                    payload = command.get_payload()
                    subcmd = payload['subcommand']
                    subcmd_payload = subcmd.get_payload()
                    item = subcmd_payload['order']
                    amnt_str += "%d |" % (item.get_amount())
                if amnt_str is not "":
                    logging.info("[Bid] [%0.2f] - %s",bid.get_value(),amnt_str)




    def __init__(self,
                 nm,id,exchange):
        self.name = nm
        self.id   = id
        self.exchange = exchange

        self.messageq = queue.Queue()

        self.thread_handle = threading.Thread(target=self.keeper_thread_function, args=(nm,))
        self.thread_handle.start()

    def __del__(self):
        self.name = ""

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def send_message(self, message):
        self.messageq.put(message)

