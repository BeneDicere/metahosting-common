from copy import copy

from metahosting.common import get_uuid
from metahosting.common.persistence import AbstractKVStore


class Store(AbstractKVStore):

    def update_config(self, values):
        pass

    def update(self, name, value):
        self.collection[name] = copy(value)

    def insert(self, value):
        self.collection[get_uuid()] = copy(value)

    def get(self, name):
        if name not in self.collection:
            return None
        return copy(self.collection[name])

    def get_all(self):
        return copy(self.collection)

    def remove(self, name):
        if name in self.collection:
            self.collection.pop(name)

    def initialize_collection(self):
        return dict()
