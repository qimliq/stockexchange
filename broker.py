import logging
import queue
import threading

from command import Command
from constants import RESPONSE

class Broker:

    id = None
    assets = []
    thread_handle = ""
    messageq = None
    latest_price = None
    exchange = None

    def process_command(self, cmd):

        type = cmd.get_type()

        if type != RESPONSE:
            payload = {"broker":self, "subcommand":cmd}
            exchange_cmd = Command(type=type, payload=payload)
            self.exchange.send_message(exchange_cmd)
        else:
            print("to investor")


    def broker_thread_function(self,id):
        while True:
            command = self.messageq.get()

            logging.info("[Broker][New command] Type: %d", command.get_type())

            self.process_command(command)

    def __init__(self,
                 id, exchange):

        self.id = id
        self.exchange = exchange

        self.messageq = queue.Queue()
        self.thread_handle = threading.Thread(target=self.broker_thread_function, args=(id,))
        self.thread_handle.start()

    def __del__(self):
        self.id = ""

    def get_id(self):
        return self.id

    def send_message(self, message):
        self.messageq.put(message)

