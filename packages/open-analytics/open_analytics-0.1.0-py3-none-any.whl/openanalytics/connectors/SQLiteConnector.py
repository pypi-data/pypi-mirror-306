from openanalytics.connectors import ConnectorInterface
import sqlite3
from sqlite3 import Cursor
from openanalytics.models import Identify, Log, Page, Token, Track
import logging


class SQLiteConnector(ConnectorInterface.ConnectorInterface):
    db: str
    client: str = None
    cursor: Cursor = None

    log = logging.getLogger("open-analytics")

    def __init__(self, db: str):

        self.log.debug("SQLiteConnector initiated.")
        self.db = db
        self._create_tables()

    def _connect(self):
        self.client = sqlite3.connect(self.db)
        self.cursor = self.client.cursor()
        self.log.debug("SQLite connection opened")

    def _disconnect(self):
        self.client = None
        self.cursor = None
        self.log.debug("SQLite connection closeds")

    def _create_tables(self):
        self._connect()
        if self._check_table_exists(Log.SIGNATURE) is None:
            self._create_log_table()
            self.log.debug(f"{Log.SIGNATURE} table created.")

        if self._check_table_exists(Identify.SIGNATURE) is None:
            self._create_identify_table()
            self.log.debug(f"{Identify.SIGNATURE} table created.")

        if self._check_table_exists(Page.SIGNATURE) is None:
            self._create_page_table()
            self.log.debug(f"{Page.SIGNATURE} table created.")

        if self._check_table_exists(Token.SIGNATURE) is None:
            self._create_token_table()
            self.log.debug(f"{Token.SIGNATURE} table created.")

        if self._check_table_exists(Track.SIGNATURE) is None:
            self._create_track_table()
            self.log.debug(f"{Track.SIGNATURE} table created.")

        self._disconnect()

    def _check_table_exists(self, table: str):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print(result)
        return result

    def _create_log_table(self):
        self.cursor.execute(
            """CREATE TABLE log
         (messageId TEXT PRIMARY KEY     NOT NULL,
         summary           TEXT    NOT NULL,
         level           TEXT    NOT NULL,
         event           TEXT    NOT NULL,
         metadata           BLOB,
         time           TEXT    NOT NULL,
         timestamp           TEXT    NOT NULL,
         type           TEXT    NOT NULL
         );"""
        )

    def _create_identify_table(self):
        self.cursor.execute(
            """CREATE TABLE identify
         (messageId TEXT PRIMARY KEY     NOT NULL,
         userID           TEXT    NOT NULL,
         event           TEXT    NOT NULL,
         metadata           BLOB,
         time           TEXT    NOT NULL,
         timestamp           TEXT    NOT NULL,
         type           TEXT    NOT NULL
         );"""
        )

    def _create_page_table(self):
        self.cursor.execute(
            """CREATE TABLE page
         (messageId TEXT PRIMARY KEY     NOT NULL,
         name           TEXT    NOT NULL,
         category           TEXT    NOT NULL,
         properties           BLOB,
         metadata           BLOB,
         time           TEXT    NOT NULL,
         timestamp           TEXT    NOT NULL,
         type           TEXT    NOT NULL
         );"""
        )

    def _create_token_table(self):
        self.cursor.execute(
            """CREATE TABLE token
         (messageId TEXT PRIMARY KEY     NOT NULL,
         event           TEXT    NOT NULL,
         action           TEXT    NOT NULL,
         count           INTEGER    NOT NULL,
         metadata           BLOB,
         time           TEXT    NOT NULL,
         timestamp           TEXT    NOT NULL,
         type           TEXT    NOT NULL
         );"""
        )

    def _create_track_table(self):
        self.cursor.execute(
            """CREATE TABLE track
         (messageId TEXT PRIMARY KEY     NOT NULL,
         endpoint           TEXT    NOT NULL,
         event           TEXT    NOT NULL,
         properties           BLOB,
         metadata           BLOB,
         time           TEXT    NOT NULL,
         timestamp           TEXT    NOT NULL,
         type           TEXT    NOT NULL
         );"""
        )

    def _insert(self, table_name, msg: dict) -> bool:
        _columns = ""
        _values = ""
        for key, value in msg.items():
            _columns += f"{key},"
            _values += f'"{value}",'

        insert_query = (
            f"insert into {table_name} ({_columns[:-1]}) values ({_values[:-1]})"
        )

        self.client.execute(insert_query)
        self.client.commit()

        self.log.debug(f"{table_name} - {msg} record inserted.")

        # on failure .commit will throw exception
        return True

    def load(self, collection_name: str, msg: dict) -> bool:
        self._connect()
        result = None

        result = self._insert(collection_name, msg)

        self._disconnect()
        return result

    def bulk_load(self, collection_name, msg) -> list[bool]:
        self._connect()
        result = []
        for record in msg:
            result.append(self._insert(collection_name, record))
        self._disconnect()
        return result
