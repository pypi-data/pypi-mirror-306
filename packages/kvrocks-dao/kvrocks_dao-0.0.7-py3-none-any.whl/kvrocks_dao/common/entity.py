from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Type, List
from datetime import datetime

T = TypeVar("T", bound="BaseEntity")


class BaseEntity(ABC):
    def __init__(self, _id: int):
        self._id = _id

    # @abstractmethod
    def to_dict(self) -> dict:
        return {key: value for key, value in vars(self).items()}

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        return cls(**data)
