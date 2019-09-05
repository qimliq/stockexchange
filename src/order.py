BID_TYPE = 0
ASK_TYPE = 1


class Order:
    order_type = BID_TYPE
    order_value = 0
    order_amount = 0

    def __init__(self, type, value, amount):
        self.order_type = type
        self.order_value = value
        self.order_amount = amount

    def get_type(self):
        return self.order_type

    def get_type_str(self):
        if self.order_type == 0:
            return "Bid"
        else:
            return "Ask"

    def get_value(self):
        return self.order_value

    def get_amount(self):
        return self.order_amount

    def set_amount(self, amount):
        self.order_amount = amount

