"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
import random
import threading
class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        # dictionar care retine id-urile producatorilor
        # si lista produselor fiecaruia publicate in marketplace
        self.producersdict = {}
        # dictionar care retine id-urile producatorilor si lista
        # de produse cumparate de le fiecare dintre ei
        self.producersbpdict = {}
        # dictionar care retine id-urile carturilor consumatorilor
        # si produsele adaugate de fiecare in cart
        self.consumersdict = {}
        self.lock = threading.Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.lock:
            rand = random.randrange(1000000)
        producer_id = str(rand)
        if producer_id in self.producersdict:
            self.register_producer()
        else:
            # creez o lista goala de produse care au fost publicate
            # si o lista goala de produse in care se vor pune cele cumparate
            self.producersdict[producer_id] = []
            self.producersbpdict[producer_id] = []
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # verific daca producatorul exista in dictionar
        if self.producersdict[producer_id] is not None:
            if len(self.producersdict[producer_id]) > self.queue_size_per_producer:
                return False
            self.producersdict[producer_id].append(product)
            return True
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock:
            cart_id = random.randrange(1000000)
        if cart_id in self.consumersdict:
            self.new_cart()
        else:
            self.consumersdict[cart_id] = []
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for key in self.producersdict:
            prods = self.producersdict[key]
            for prod in prods:
                # cand gasesc produsul dorit la un producator
                if prod == product:
                    self.consumersdict[cart_id].append(product)
                    self.producersbpdict[key].append(product)
                    self.producersdict[key].remove(prod)
                    return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # verific daca cosul exista in dictionar
        if cart_id in self.consumersdict:
            if product in self.consumersdict[cart_id]:
                self.consumersdict[cart_id].remove(product)
                for key in self.producersbpdict:
                    prods = self.producersbpdict[key]
                    for prod in prods:
                        # readaug produsul in coada producatorului
                        # daca consumerul il sterge din cart
                        if prod == product:
                            self.producersbpdict[key].remove(product)
                            self.producersdict[key].append(product)


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.consumersdict[cart_id]
