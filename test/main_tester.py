import logging
import time
from src.book_keeper import BookKeeper
from src.order import Order, BID_TYPE, ASK_TYPE
import random

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating keeper")

    keeper = BookKeeper("test")

    for i in range(2):
        logging.info("---------------------------------%d",i)
        type = 1
        value = 5.5
        amount = 1000
        order = Order(type, value, amount)
        keeper.send_message(order)
        time.sleep(1)

    for i in range(10):
        logging.info("---------------------------------%d",i)
        type = 0
        value = 5.5
        amount = 200
        order = Order(type, value, amount)
        keeper.send_message(order)
        time.sleep(1)

    for i in range(100):
        logging.info("---------------------------------%d",i)
        type = random.randint(0,1)
        value = round(random.uniform(4,6),1)
        amount = random.randint(100,10000)
        order = Order(type, value, amount)
        keeper.send_message(order)
        time.sleep(1)

    logging.info("Main    : all done")


