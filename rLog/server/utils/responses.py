import json
from abc import ABCMeta
from typing_extensions import Literal


class SrvResp(metaclass=ABCMeta):
    resp_type: Literal["ACK", "NACK"]

    def __init__(self, msg: str):
        self.msg = msg

    def to_json(self):
        return json.dumps(
            {
                "resp": self.resp_type,
                "msg": self.msg
            }
        )

    def to_bytes(self):
        return bytes(self.to_json(), "utf8")


class Error(SrvResp):
    resp_type = "NACK"


class Valid(SrvResp):
    resp_type = "ACK"
