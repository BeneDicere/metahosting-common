from datetime import datetime
from pymongo import MongoClient
from retrying import retry

from metahosting.common.persistence import AbstractKVStore


class MongoStore(AbstractKVStore):
    def initialize_collection(self):
        url = 'mongodb://{}:{}/{}'.format(
            self.get_property('host'),
            int(self.get_property('port')),
            self.get_property('database'))
        return self._initialize_connection(url)

    @retry(stop_max_attempt_number=10, wait_fixed=1000)
    def _initialize_connection(self, url):
        client = MongoClient(host=url)
        return client[
            self.get_property('database')][self.get_property('collection')]

    def update(self, name, value):
        self.collection.replace_one(filter={'name': name},
                                    replacement={'name': name, 'value': value},
                                    upsert=True)

    def insert(self, value):
        if 'ts' not in value.keys():
            value['ts'] = datetime.now()
        self.collection.insert_one(document=value)
