from typing import TypeVar, Generic, Type, List
from redis import Redis
from kvrocks_dao import BaseEntity
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

host = config["kvrocks"]["host"]
port = config["kvrocks"]["port"]

T = TypeVar("T", bound=BaseEntity)


class BaseDAO(Generic[T]):
    def __init__(self, entity_cls: Type[T], name):
        self.entity_cls = entity_cls
        self.name = name
        self.conn = None
        self.prefix = f"{self.name}_*"

        if self.conn == None:
            self.conn = Redis(host=host, port=port, decode_responses=True)
            print(f"[KvrocksDAO][{self.name}] Connected to kvrocks on port {port}")

    def __del__(self):
        self.conn.close()
        print(f"[KvrocksDAO][{self.name}] Connection closed")

    @classmethod
    def from_entity(cls, entity_cls: Type[T], name: str) -> "BaseDAO[T]":
        """Class method to create a DAO for a specific entity class."""
        return cls(entity_cls, name)

    def _get(self, key: str):
        json_data = self.conn.get(key)

        if json_data == None:
            return None
        return self.entity_cls.from_dict(json.loads(json_data))

    def get_key(self, _id: int):
        return f"{self.name}_{_id}"

    def set(self, enity: T):
        key = self.get_key(enity._id)
        return self.conn.set(key, json.dumps(enity.to_dict()))

    def get(self, _id: int) -> T:
        return self._get(self.get_key(_id))

    def mget(self, limit: int = None) -> List[tuple[int, T]]:
        cursor = 0
        data = []

        while True:
            cursor, keys = self.conn.scan(cursor=cursor, match=self.prefix)

            for key in keys:
                entity = self._get(key)
                if entity is not None:
                    data.append((entity._id, self._get(key)))
                if limit is not None and len(data) >= limit:
                    break

            if cursor == 0:
                break

        return data

    def delete(self, _id: int):
        self.conn.delete(self.get_key(_id))

    def count(self) -> int:
        count = 0
        cursor = 0

        while True:
            cursor, keys = self.conn.scan(cursor=cursor, match=self.prefix)
            count += len(keys)

            # Break if cursor is 0, which means the scan is complete
            if cursor == 0:
                break

        return count
