"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time
import threading

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        Thread.__init__(self, **kwargs)
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.cart_id = self.marketplace.new_cart()
        self.name = kwargs["name"]
        self.lock = threading.Lock()

    def run(self):
        for cart in self.carts:
            for piece in cart:
                quantity = piece['quantity']
                prod = piece['product']
                if piece['type'] == "add":
                    while quantity != 0:
                        success = self.marketplace.add_to_cart(self.cart_id, prod)
                        # incerc sa adaug in cos pana cand gasesc produsul in marketplace
                        while not success:
                            # astept retry_wait_time de fiecare data cand nu reusesc
                            time.sleep(self.retry_wait_time)
                            success = self.marketplace.add_to_cart(self.cart_id, prod)
                        with self.lock:
                            quantity = quantity - 1
                elif piece['type'] == "remove":
                    while quantity != 0:
                        self.marketplace.remove_from_cart(self.cart_id, prod)
                        with self.lock:
                            quantity = quantity - 1
        # obtin lista de produse din cart a consumerului
        products = self.marketplace.place_order(self.cart_id)
        for product in products:
            print(self.name + " bought " + str(product))
            