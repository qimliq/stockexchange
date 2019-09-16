import logging
import queue
import threading

class Broker:

    id = None
    assets = []
    thread_handle = ""
    messageq = queue.Queue()
    latest_price = None
    exchange = None

    def process_command(self, cmd):
        return 0

    def broker_thread_function(self,id):
        while True:
            command = self.messageq.get()

            logging.info("[Broker][New command] Type: %d", command.get_type())

            self.process_command(command)

    def __init__(self,
                 id, exchange):

        self.id = id
        self.exchange = exchange
        self.thread_handle = threading.Thread(target=self.broker_thread_function, args=(id,))
        self.thread_handle.start()

    def __del__(self):
        self.id = ""

    def get_id(self):
        return self.id

    def send_message(self, message):
        self.messageq.put(message)

