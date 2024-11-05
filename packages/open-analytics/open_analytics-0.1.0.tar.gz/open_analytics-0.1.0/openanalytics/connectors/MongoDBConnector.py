from openanalytics.checklibs import pkg_install

pkg_install("pymongo")

from pymongo import MongoClient
from pymongo.results import InsertManyResult, InsertOneResult
from openanalytics.connectors.ConnectorInterface import ConnectorInterface
import logging
from openanalytics.version import APP_NAME


class MongoDBConnector(ConnectorInterface):
    host: str
    db: str
    client: MongoClient = None

    log = logging.getLogger(APP_NAME)

    def __init__(self, host, dbname):
        self.host = host
        self.db = dbname

    def _connect(self):
        self.client = MongoClient(self.host)
        self.log.debug("MongoDB connection opened")

    def _disconnect(self):
        self.client.close()
        self.log.debug("MongoDB connection closed")

    def load(self, collection_name: str, msg: dict) -> InsertOneResult:

        self._connect()
        _client = self.client
        _db = _client[self.db]
        _collection = _db[collection_name]
        result = _collection.insert_one(msg)
        self._disconnect()
        self.log.debug(f"{collection_name} - {msg} record inserted.")

        return result

    def bulk_load(self, collection_name, msg) -> InsertManyResult:

        self._connect()
        _client = self.client
        _db = _client[self.db]
        _collection = _db[collection_name]
        result = _collection.insert_many(msg, ordered=True)
        self._disconnect()
        self.log.debug(f"{collection_name} - {len(msg)} records inserted.")

        return result
