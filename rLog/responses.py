import json
from abc import ABCMeta
from typing_extensions import Literal


class SrvResp(metaclass=ABCMeta):
    resp_type = Literal["ACK", "NACK"]

    def __new__(cls, msg: str):
        return bytes(
            json.dumps(
                {
                    "resp": cls.resp_type,
                    "msg": msg
                }
            ).encode("utf8")
        )


class Error(SrvResp):
    resp_type = "NACK"


class Valid(SrvResp):
    resp_type = "ACK"
