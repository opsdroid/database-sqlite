import logging
import json
import sqlite3

from opsdroid.database import Database


class DatabaseSqlite(Database):
    """A module for opsdroid to allow persist in a sqlite database."""

    def __init__(self, config):
        """Start the database connection."""
        logging.debug("Loaded sqlite database connector")
        self.name = "sqlite"
        self.config = config
        self.conn = None
        self.table = None

    async def connect(self, opsdroid):
        """Connect to the database."""
        db_file = self.config.get("file", "sqlite.db")
        table = self.config.get("table", "opsdroid")

        self.conn = sqlite3.connect(db_file, isolation_level=None)
        self.table = table
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS {} (key text PRIMARY KEY, data text)"
            .format(self.table)
        )
        logging.info("Connected to sqlite {}".format(db_file))

    async def put(self, key, data):
        """Insert or replace an object into the database for a given key."""
        logging.debug("Putting " + key + " into sqlite")
        json_data = json.dumps(data)
        cur = self.conn.cursor()
        cur.execute(
            "DELETE FROM {} WHERE key=?".format(self.table), (key,))
        cur.execute(
            "INSERT INTO {} VALUES (?, ?)".format(self.table),
            (key, json_data))
        cur.close()

    async def get(self, key):
        """Get data from the database for a given key."""
        logging.debug("Getting " + key + " from sqlite")
        data = None
        cur = self.conn.cursor()
        cur.execute(
            "SELECT data FROM {} WHERE key=?".format(self.table), (key,))
        row = cur.fetchone()
        if row:
            data = json.loads(row[0])
        cur.close()
        return data
