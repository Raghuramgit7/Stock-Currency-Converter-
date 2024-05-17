from .Model import Model
from datetime import datetime
from google.cloud import datastore


def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    This returns:
        [ quote, name, dateofquote, sourcetype, sourcequote, rating ]
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['quote'], entity['name'], entity['dateofquote'], entity['sourcetype'], entity['sourcequote'], entity['rating']]


class model(Model):
    def __init__(self):
        self.client = datastore.Client('cloud-nataraja-raghuram')

    def select(self):
        query = self.client.query(kind = 'hw4_quotes')
        print("query: ", query)
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self, id, quote, name, dateofquote, sourcetype, sourcequote, rating):
        key = self.client.key('hw4_quotes')
        rev = datastore.Entity(key)
        print("-----: ",key, rev )
        rev.update( {
            "id": id,
            "quote": quote, 
            "name": name, 
            "dateofquote": dateofquote, 
            "sourcetype": sourcetype, 
            "sourcequote": sourcequote, 
            "rating": rating
            })
        self.client.put(rev)
        return True