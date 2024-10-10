import json
import socket
from rLog.client import logger


class ClientBasic:
    def __init__(self, client_id: str, host: str, port: int):
        self.cli_id = client_id
        self.host = host
        self.port = port

    def _serialize(self, msg: dict) -> bytes:
        return bytes(json.dumps(msg), "ascii")

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        logger.info("socket connect")

    def send(self, msg: dict):
        self.s.sendall(self._serialize(dict(msg)))
        resp = self.s.recv(1024)
        logger.debug(f"server response: {resp}")

        if not resp:
            return "remote is offline"
        else:
            return resp

    def close(self):
        self.s.close()
        logger.info("socket disconnect")


if __name__ == "__main__":
    pass
