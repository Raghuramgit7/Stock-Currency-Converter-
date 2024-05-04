"""
Python list model
"""
from datetime import date
from .Model import Model

class model(Model):
    def __init__(self):
        self.guestentries = []

    def select(self):
        """
        Returns guestentries list of lists
        Each list in guestentries contains: name, email, date, message
        :return: List of lists
        """
        return self.guestentries 

    def insert(self, id, quote, name, dateofquote, sourcetype, sourcequote, rating):
        """
        Appends a new list of values representing new message into guestentries
        :param quote: String
        :param name: String
        :param dateofquote: date
        :param sourcetype: String
        :param sourcequote: String
        :param rating: Integer
        :return: True
        """
        params = [id, quote, name, dateofquote, sourcetype, sourcequote, rating]
        self.guestentries.append(params)
        return True
