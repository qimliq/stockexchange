import logging
import random
import time
from decimal import *

from book_keeper import BookKeeper
from order import Order

getcontext().prec = 2
from os import system

BID_TYPE = 0
ASK_TYPE = 1


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating keeper")

    keeper = BookKeeper("test")

    value = 6.0
    for i in range(10):
        logging.info("---------------------------------%d",i)
        type = ASK_TYPE
        amount = 1000
        order = Order(type, value, amount)
        keeper.send_message(order)
        order = Order(type, value, amount)
        keeper.send_message(order)
        value = value - 0.1
        time.sleep(0.25)

    # value = 5.0
    # order = Order(BID_TYPE, value, 500)
    # keeper.send_message(order)

    value = 4.0
    for i in range(10):
        logging.info("---------------------------------%d",i)
        type = BID_TYPE
        amount = 1000
        order = Order(type, value, amount)
        keeper.send_message(order)
        order = Order(type, value, amount)
        keeper.send_message(order)
        value = value + 0.1
        time.sleep(0.25)

    value = round(5.90,2)
    for i in range(1):
        logging.info("---------------------------------%d", i)
        type = BID_TYPE
        amount = 1200
        order = Order(type, value, amount)
        keeper.send_message(order)
        # value = value + 0.1
        time.sleep(0.25)


    for k in range(100):

        value = round(4.00, 2)
        type = ASK_TYPE
        amount = 1000000
        order = Order(type, value, amount)
        keeper.send_message(order)


        for i in range(1000):
            system('clear')
            logging.info("0-----------------%d---------------%d",k,i)
            type = random.randint(0,1)
            value = round(random.uniform(4,6),1)
            amount = random.randint(100,10000)
            # amount = random.randint(1,10) * 100
            order = Order(type, value, amount)
            keeper.send_message(order)
            time.sleep(0.1)


        value = round(6.00, 2)
        type = BID_TYPE
        amount = 1000000
        order = Order(type, value, amount)
        keeper.send_message(order)

        for i in range(1000):
            system('clear')
            logging.info("1-----------------%d---------------%d", k, i)
            type = random.randint(0,1)
            value = round(random.uniform(4,6),1)
            amount = random.randint(100,10000)
            # amount = random.randint(1,10) * 100
            order = Order(type, value, amount)
            keeper.send_message(order)
            time.sleep(0.1)

    logging.info("Main    : all done")


