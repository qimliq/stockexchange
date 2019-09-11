import logging
import queue
import threading

class Broker:

    id = None
    investors = []

    def __init__(self,
                 id):
        self.id = id

