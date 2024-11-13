import os
from typing import Any
from redis.asyncio import Redis


class Storage:
    def __init__(self):
        self.conn = Redis(host=os.environ.get("REDIS"))

    def get_connect(self):
        return self.conn


def connect_redis():
    db = Storage()
    return db.get_connect()