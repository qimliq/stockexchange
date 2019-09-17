import logging
import queue
import threading
from book_keeper import BookKeeper
from constants import NEW_ORDER,EDIT_ORDER,CANCEL_ORDER,GET_LAST_PRICE,RESPONSE

class Exchange:

    name = "TestExchange"
    assets = []
    thread_handle = ""
    messageq = queue.Queue()
    latest_price = None

    def find_book_keeper(self,id):
        bookkeeper = None
        for keeper in self.assets:
            keeper_id = keeper.get_id()
            if keeper_id == id:
                bookkeeper = keeper
                break
        return bookkeeper

    def process_command(self, cmd):
        type = cmd.get_type()

        if type != RESPONSE:
            payload = cmd.get_payload()
            subcmd = payload['subcommand']

            subcmd_payload = subcmd.get_payload()

            investor_id = subcmd_payload['investor']
            order = subcmd_payload['order']

            asset_id = order.get_asset_id()

            keeper = self.find_book_keeper(asset_id)

            if keeper != None:
                keeper.send_message(cmd)
        else:
            print("to broker")

        return 0

    def exchange_thread_function(self,name):
        while True:
            command = self.messageq.get()

            logging.info("[Exchange] [New command] Type: %d", command.get_type())

            self.process_command(command)

    def __init__(self,
                 nm,
                 asset_names):
        for asset in asset_names:
            keeper = BookKeeper(nm=asset['name'], id=asset['id'])
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

