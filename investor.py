import logging
import queue
import threading

from constants import *
from command import Command
from order import Order
from broker import Broker

class Investor:

    id = None
    broker = None
    capital = 0

    assets = []
    orders = []

    thread_handle = None
    messageq = queue.Queue()
    money_in_stock = 0

    def process_command(self, cmd):
        return 0

    def investor_thread_function(self,id):
        while True:
            command = self.messageq.get()

            logging.info("[New command] Type: %d", command.get_type())

            self.process_command(command)

    def __init__(self,
                 id, cap, broker):

        self.id = id
        self.capital = cap
        self.broker = broker

        self.thread_handle = threading.Thread(target=self.investor_thread_function, args=(id,))
        self.thread_handle.start()

    def __del__(self):
        self.id = None

    def get_id(self):
        return self.id

    def send_message(self, message):
        self.messageq.put(message)

    def add_asset(self, asset):
        for iasset in self.assets:
            if iasset.name == asset.name:
                return
        self.assets.append(asset)

    def buy(self, assetid, price, amount):
        order = Order(type=BID_TYPE, assetid=assetid, value=price, amount=amount)
        payload = {"investor":id, "order":order}
        cmd = Command(type=NEW_ORDER,payload=payload)
        self.broker.send_message(cmd)

    def sell(self, assetid, price, amount):
        order = Order(type=ASK_TYPE, assetid=assetid, value=price, amount=amount)
        payload = {"investor": id, "order": order}
        cmd = Command(type=NEW_ORDER,payload=payload)
        self.broker.send_message(cmd)
