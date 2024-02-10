from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class Message:
    timestamp: int
    device_id: str
    streams: list
    payload: dict


class Endpoint(metaclass=ABCMeta):
    def __init__(self):
        pass

    def run_process(self):
        raise NotImplementedError

    def kill_process(self):
        # join child spawned processes
        raise NotImplementedError
