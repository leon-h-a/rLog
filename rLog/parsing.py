import json


def serialize(ts: int, device_id: str, streams: list, payload: dict) -> bytes:
    return bytes(json.dumps(
        dict(
            ts=ts,
            device_id=device_id,
            streams=streams,
            payload=payload
        )
    ), "ascii")
