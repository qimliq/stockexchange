import logging
import time
from src.book_keeper import BookKeeper
from src.order import Order, BID_TYPE, ASK_TYPE
import random
from decimal import *
getcontext().prec = 2

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating keeper")

    keeper = BookKeeper("test")

    value = 5.0
    for i in range(10):
        logging.info("---------------------------------%d",i)
        type = 1
        amount = 1000
        order = Order(type, value, amount)
        keeper.send_message(order)
        value = value + 0.1
        time.sleep(0.25)

    value = 4.0
    for i in range(10):
        logging.info("---------------------------------%d",i)
        type = 0
        amount = 1000
        order = Order(type, value, amount)
        keeper.send_message(order)
        value = value + 0.1
        time.sleep(0.25)

    value = round(4.50,2)
    for i in range(50):
        logging.info("---------------------------------%d", i)
        type = 1
        amount = 100
        order = Order(type, value, amount)
        keeper.send_message(order)
        # value = value + 0.1
        time.sleep(0.25)

    for i in range(100000):
        logging.info("---------------------------------%d",i)
        type = random.randint(0,1)
        value = round(random.uniform(4,6),1)
        amount = random.randint(100,10000)
        amount = random.randint(1,10) * 100
        order = Order(type, value, amount)
        keeper.send_message(order)
        time.sleep(0.25)

    logging.info("Main    : all done")


