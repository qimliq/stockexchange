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

    investor1 = Investor(id=2000,cap=100000,broker=broker)

    for i in range(1):
        investor1.buy(assetid=1,price=5.0,amount=1000)

    investor2 = Investor(id=2001, cap=100000, broker=broker)

    for i in range(5):
        investor2.sell(assetid=1, price=5.0, amount=100)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    test_exchange()

