from dataclasses import dataclass
from abc import ABCMeta


class Stream(metaclass=ABCMeta):
    _id = None

    def __init__(self, streamname: str):
        self._streamname = streamname

    def validate(self, payload: str):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError


@dataclass
class ServerResponse:
    text: str
