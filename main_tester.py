import logging
import random
import time
from decimal import *

from book_keeper import BookKeeper
from exchange import Exchange
from order import Order
from broker import Broker
from command import Command
from investor import Investor
from constants import NEW_ORDER,CANCEL_ORDER,GET_LAST_PRICE,RESPONSE,EDIT_ORDER,ASK_TYPE,BID_TYPE

getcontext().prec = 2
from os import system

BID_TYPE = 0
ASK_TYPE = 1

def test_bookkeeper():
    logging.info("Main    : before creating keeper")

    keeper = BookKeeper("test")

    value = 6.0
    for i in range(10):
        logging.info("---------------------------------%d", i)
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
        logging.info("---------------------------------%d", i)
        type = BID_TYPE
        amount = 1000
        order = Order(type, value, amount)
        keeper.send_message(order)
        order = Order(type, value, amount)
        keeper.send_message(order)
        value = value + 0.1
        time.sleep(0.25)

    value = round(5.90, 2)
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
        amount = random.randint(0, 4) * 1000000
        order = Order(type, value, amount)
        keeper.send_message(order)

        for i in range(1000):
            system('clear')
            logging.info("0-----------------%d---------------%d", k, i)
            type = random.randint(0, 1)
            value = round(random.uniform(4, 6), 1)
            amount = random.randint(100, 10000)
            # amount = random.randint(1,10) * 100
            order = Order(type, value, amount)
            keeper.send_message(order)
            time.sleep(0.1)

        value = round(6.00, 2)
        type = BID_TYPE
        amount = random.randint(0, 4) * 1000000
        order = Order(type, value, amount)
        keeper.send_message(order)

        for i in range(1000):
            system('clear')
            logging.info("1-----------------%d---------------%d", k, i)
            type = random.randint(0, 1)
            value = round(random.uniform(4, 6), 1)
            amount = random.randint(100, 10000)
            # amount = random.randint(1,10) * 100
            order = Order(type, value, amount)
            keeper.send_message(order)
            time.sleep(0.1)

    logging.info("Main    : all done")

def test_exchange():
    asset_names = [{'name': "Asset 1", 'id': 1},
                   {'name': "Asset 2", 'id': 2},
                   {'name': "Asset 3", 'id': 3},
                   {'name': "Asset 4", 'id': 4},
                   {'name': "Asset 5", 'id': 5},
                   {'name': "Asset 6", 'id': 6},
                   {'name': "Asset 7", 'id': 7},
                   {'name': "Asset 8", 'id': 8}]

    exchange = Exchange("TestExchange", asset_names=asset_names)

    broker = Broker(id=1000,exchange=exchange)

    investor = Investor(id=2000,cap=100000,broker=broker)

    investor.buy(assetid=1,price=5.0,amount=1000)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # test_bookkeeper()
    test_exchange()

