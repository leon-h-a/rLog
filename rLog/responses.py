from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class SrvResp(metaclass=ABCMeta):
    text: str

    def __init__(self, text: str):
        self.text = text


class Error(SrvResp):
    pass


class Valid(SrvResp):
    pass
