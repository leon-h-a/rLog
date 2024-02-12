from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class Message:
    # ts, dev_id and streams are must have
    # payload is dict that can have variable
    # number of k-v pairs
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
