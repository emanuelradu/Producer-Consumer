"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import threading
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):

        Thread.__init__(self, **kwargs)
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = self.marketplace.register_producer()
        self.lock = threading.Lock()

    def run(self):
        while True:
            for product in self.products:
                i = product[1]
                while i != 0:
                    prod = product[0]
                    success = self.marketplace.publish(self.producer_id, prod)
                    # daca am reusit sa public,
                    # astept pama cand pot produce urmatorul produs
                    if success:
                        time.sleep(product[2])
                    # incerc sa public pana cand unul sau mai multe locuri
                    # in coada de produse se elibereaza
                    while not success:
                        time.sleep(self.republish_wait_time)
                        success = self.marketplace.publish(self.producer_id, prod)
                        if success:
                            time.sleep(product[2])
                    with self.lock:
                        i = i - 1
                        