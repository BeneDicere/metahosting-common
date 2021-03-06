from abc import ABCMeta, abstractmethod


class AbstractKVStore(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self.settings = dict()
        if 'config' in kwargs:
            self.config_update(kwargs['config'])
        self.collection = self.initialize_collection()

    @abstractmethod
    def initialize_collection(self):
        pass

    @abstractmethod
    def update(self, name, value):
        pass

    @abstractmethod
    def insert(self):
        pass

    def get(self, name):
        element = self.collection.find_one({'name': name})
        if element is None:
            return None
        return element['value']

    def get_all(self):
        return {
            i['name']: i['value'] for i in self.collection.find()
        }

    def config_update(self, settings):
        for k, v in settings.iteritems():
            self.set_property(k, v)

    def set_property(self, key, value):
        self.settings[key] = value

    def get_property(self, key):
        if key in self.settings:
            return self.settings[key]
        else:
            return None
