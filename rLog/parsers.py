import json
from rLog import logger
from rLog.models import Message


def serialize(timestamp: int, device_id: str, streams: list, **payload) -> bytes:
    # Data can be omitted as system could be used as keepalive
    stringed = json.dumps(
        dict(
            timestamp=timestamp,
            device_id=device_id,
            streams=streams,
            payload=payload
        )
    )
    logger.debug(stringed)
    return bytes(stringed, "ascii")


def deserialize(data: bytes) -> Message:
    # If Data field is omitted, msg shall be treated as keepalive
    loaded = json.loads(data.decode('utf8').replace("'", '"'))
    logger.debug(loaded)
    return Message(
        timestamp=loaded["timestamp"],
        device_id=loaded["device_id"],
        streams=loaded["streams"],
        payload=loaded["payload"]
    )
