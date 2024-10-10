import json
from abc import ABCMeta
from typing_extensions import Literal


class SrvResp(metaclass=ABCMeta):
    resp_type = Literal["ACK", "NACK"]

    def __new__(cls, msg: str, byte_rep: bool = True):
        resp = json.dumps(
                {
                    "resp": cls.resp_type,
                    "msg": msg
                }
            )

        if byte_rep:
            return bytes(resp, "utf8")
        else:
            # Used when multiple dumps are concatenated to a single response
            return resp


class Error(SrvResp):
    resp_type = "NACK"


class Valid(SrvResp):
    resp_type = "ACK"
