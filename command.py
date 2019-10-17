from decimal import *
getcontext().prec =2

class Command:
    type = None
    payload = None
    response = None

    def __init__(self, type, payload=None):
        self.type = type
        self.payload = payload

    def get_type(self):
        return self.type

    def get_payload(self):
        return self.payload

