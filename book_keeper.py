import logging
import queue
import threading

from order_container import OrderContainer
from command import Command
from constants import BID_TYPE, ASK_TYPE, NEW_ORDER, CANCEL_ORDER, EDIT_ORDER, RESPONSE, RESPONSE_ACK, \
                      ORDER_NOT_MATCHED, ORDER_PARTIALLY_MATCHED, ORDER_FULLY_MATCHED, \
                      RESPONSE_ORDER_FULLY_MATCHED, RESPONSE_ORDER_PARTIALLY_MATCHED, RESPONSE_ORDER_CANCELLED, \
                      RESPONSE_ORDER_EDITED


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

    def process_ask_order(self,order,cmd):
        def sorter_fcn(a):
            c = a.get_value()
            return c
        value = order.get_value()
        amount = order.get_amount()
        new_ask = True
        matched = ORDER_NOT_MATCHED

        for i in range(len(self.bids)):
            bid_container = self.bids[i]
            if value <= bid_container.get_value():
                for command in list(bid_container.get_orders().queue):
                    payload = command.get_payload()
                    subcmd = payload['subcommand']
                    subcmd_payload = subcmd.get_payload()

                    item = subcmd_payload['order']

                    self.latest_price = bid_container.get_value()
                    if amount < item.get_amount():
                        item.set_amount(item.get_amount() - amount)
                        amount = 0
                        # send 2 messages

                        # First - Fully Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": cmd}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        matched = ORDER_FULLY_MATCHED

                        # Second - Partially Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_PARTIALLY_MATCHED, "payload": command}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        break
                    elif amount == item.get_amount():
                        item.set_amount(item.get_amount() - amount)
                        amount = 0
                        # send 2 messages

                        # First - Fully Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": cmd}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        matched = ORDER_FULLY_MATCHED

                        # Second - Partially Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": command}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        break
                    else:
                        amount = amount - item.get_amount()
                        item.set_amount(0)
                        order.set_amount(amount)
                        bid_container.get_next_order()
                        # send 2 messages

                        # First - Fully Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_PARTIALLY_MATCHED, "payload": cmd}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        matched = ORDER_PARTIALLY_MATCHED

                        # Second - Partially Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": command}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        # if bid_container.get_orders().empty() is True:
                        #     self.bids.remove(bid_container)

        if matched is ORDER_NOT_MATCHED:
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


        self.asks = sorted(self.asks, key=sorter_fcn, reverse=True)

    def process_bid_order(self,order,cmd):
        def sorter_fcn(a):
            c = a.get_value()
            return c
        value = order.get_value()
        amount = order.get_amount()

        new_bid = True
        matched = ORDER_NOT_MATCHED
        for i in range(len(self.asks)):
            ask_container = list(reversed(self.asks))[i]
            if value >= ask_container.get_value():
                for command in list(ask_container.get_orders().queue):
                    payload = command.get_payload()
                    subcmd = payload['subcommand']
                    subcmd_payload = subcmd.get_payload()

                    item = subcmd_payload['order']

                    self.latest_price = ask_container.get_value()
                    if amount < item.get_amount():
                        item.set_amount(item.get_amount() - amount)
                        amount = 0
                        #send 2 messages

                        #First - Fully Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": cmd}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        matched = ORDER_FULLY_MATCHED

                        # Second - Partially Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_PARTIALLY_MATCHED, "payload": command}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)


                        break
                    elif amount == item.get_amount():
                        item.set_amount(item.get_amount() - amount)
                        amount = 0

                        # send 2 messages

                        # First - Fully Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": cmd}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        matched = ORDER_FULLY_MATCHED

                        # Second - Partially Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": command}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)

                        break
                    else:
                        amount = amount - item.get_amount()
                        item.set_amount(0)
                        order.set_amount(amount)
                        ask_container.get_next_order()

                        # send 2 messages

                        # First - Fully Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_PARTIALLY_MATCHED, "payload": cmd}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)
                        matched = ORDER_PARTIALLY_MATCHED

                        # Second - Partially Matched
                        response_payload = {"resp_type": RESPONSE_ORDER_FULLY_MATCHED, "payload": command}
                        response = Command(type=RESPONSE, payload=response_payload)
                        self.exchange.send_message(response)

                        # if ask_container.get_orders().empty() is True:
                        #     self.asks.remove(ask_container)

        if matched is ORDER_NOT_MATCHED:
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

        self.bids = sorted(self.bids, key=sorter_fcn, reverse=True)

    def process_command(self, cmd):

        # investor : type + payload where payload: dict(investor id, order)
        # broker   : type + payload where payload: dict(broker, investor cmd)
        # exchange : broker cmd

        payload = cmd.get_payload()
        subcmd = payload['subcommand']

        subcmd_payload = subcmd.get_payload()

        order = subcmd_payload['order']
        investor_id = subcmd_payload['investor']

        type = order.get_type()
        value = order.get_value()
        amount = order.get_amount()

        cmd_type = cmd.get_type()

        logging.info("[Bookkeeper [%d]][Cmd Type: %d][Order Type:%d]", self.id, cmd_type, type)

        ##############
        # send ACK
        response_payload = {"resp_type": RESPONSE_ACK, "payload":cmd}
        response = Command(type=RESPONSE, payload=response_payload)
        self.exchange.send_message(response)

        if cmd_type == NEW_ORDER:
            if type == ASK_TYPE:
                self.process_ask_order(order,cmd)
            elif type == BID_TYPE:
                self.process_bid_order(order,cmd)
        elif cmd_type == CANCEL_ORDER:
            print("TODO")
        elif cmd_type == EDIT_ORDER:
            print("TODO")

        # self.clean_containers()

    def keeper_thread_function(self,name):
        logging.info("BookKeeper for [%s][id: %d] started", name, self.id)
        while True:
            cmd = self.messageq.get()

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

    def get_latest_price(self):
        return self.latest_price

    def send_message(self, message):
        self.messageq.put(message)

