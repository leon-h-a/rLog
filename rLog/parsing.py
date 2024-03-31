import json


def serialize(
        ts: int,
        device_id: str,
        streams: list,
        payload: dict
        ) -> bytes:

    stringed = json.dumps(
        dict(
            ts=ts,
            device_id=device_id,
            streams=streams,
            payload=payload
        )
    )
    return bytes(stringed, "ascii")
