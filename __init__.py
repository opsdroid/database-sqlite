import logging
import json
import aiosqlite

from opsdroid.database import Database


class DatabaseSqlite(Database):
    """A module for opsdroid to allow persist in a sqlite database."""

    def __init__(self, config):
        """Start the database connection."""
        logging.debug("Loaded sqlite database connector")
        self.name = "sqlite"
        self.config = config
        self.conn_args = {'isolation_level': None}
        self.db_file = None
        self.table = None

    async def connect(self, opsdroid):
        """Connect to the database."""
        self.db_file = self.config.get("file", "sqlite.db")
        self.table = self.config.get("table", "opsdroid")

        async with aiosqlite.connect(self.db_file, **self.conn_args) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS {}"
                "(key text PRIMARY KEY, data text)"
                .format(self.table)
            )
        logging.info("Connected to sqlite {}".format(self.db_file))

    async def put(self, key, data):
        """Insert or replace an object into the database for a given key."""
        logging.debug("Putting " + key + " into sqlite")
        json_data = json.dumps(data)
        async with aiosqlite.connect(self.db_file, **self.conn_args) as db:
            cur = await db.cursor()
            await cur.execute(
                "DELETE FROM {} WHERE key=?".format(self.table), (key,))
            await cur.execute(
                "INSERT INTO {} VALUES (?, ?)".format(self.table),
                (key, json_data))

    async def get(self, key):
        """Get data from the database for a given key."""
        logging.debug("Getting " + key + " from sqlite")
        data = None
        async with aiosqlite.connect(self.db_file, **self.conn_args) as db:
            cur = await db.cursor()
            await cur.execute(
                "SELECT data FROM {} WHERE key=?".format(self.table), (key,))
            row = await cur.fetchone()
            if row:
                data = json.loads(row[0])
        return data
