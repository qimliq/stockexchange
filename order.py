from constants import BID_TYPE,ASK_TYPE
from decimal import *
getcontext().prec =2



class Order:
    asset_id = None
    order_type = None
    order_value = round(0.0,2)
    order_amount = 0

    def __init__(self, assetid, type, value, amount):
        self.asset_id = assetid
        self.order_type = type
        self.order_value = value
        self.order_amount = amount

    def get_asset_id(self):
        return self.asset_id

    def get_type(self):
        return self.order_type

    def get_type_str(self):
        if self.order_type == 0:
            return "Bid"
        else:
            return "Ask"

    def get_value(self):
        return round(self.order_value,2)

    def get_amount(self):
        return self.order_amount

    def set_amount(self, amount):
        self.order_amount = amount

