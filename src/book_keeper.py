import threading
import logging
import time

class BookKeeper:

    name = "test"
    bid_list = []
    thread_handle = ""


    def keeper_thread_function(self,name):
        while True:
            time.sleep(2)
            logging.info("keeper_thread: running :%s",name)


    def __init__(self,
                 nm):
        self.name = nm
        self.thread_handle = threading.Thread(target=self.keeper_thread_function, args=(nm,))
        self.thread_handle.start()

    def __del__(self):
        self.name = ""



    def GetName(self):
        return self.name
