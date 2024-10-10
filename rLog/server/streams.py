import socket
from abc import ABCMeta
from rLog.server.utils.responses import Error, Valid


class Stream(metaclass=ABCMeta):
    name: str
    port: int
    enabled: bool
    q_sock: socket.socket = None
    required_fields = ["ts", "payload", "client_id"]

    def setup():
        """
        Create database connections or system directories.
        """
        raise NotImplementedError

    def input_sanitize(payload: dict) -> [Valid, Error]:
        """
        Checkes if all fields defined for specific stream are present in
        client payload.
        """
        raise NotImplementedError

    def output_generate(payload: dict, out_conn: any):
        """
        Defines how payload is written to storage system.
        """
        raise NotImplementedError

    def output_cleanup():
        """
        Gracefully close existing connections. If they exists.
        """
        raise NotImplementedError
