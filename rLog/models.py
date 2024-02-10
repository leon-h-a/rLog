from dataclasses import dataclass


@dataclass
class Message:
    timestamp: int
    device_id: str
    streams: list
    payload: dict
