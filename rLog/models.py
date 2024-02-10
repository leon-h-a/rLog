from dataclasses import dataclass


@dataclass
class ExchangePayload:
    timestamp: int
    device_id: str
    streams: list
    payload: dict
