import ssl
import json
import socket
from rLog import logger
from rLog.responses import SrvResp


class ClientTLS:
    def __init__(self, client_id: str, host: str, port: int, key_path: str):
        self.cli_id = client_id
        self.host = host
        self.port = port
        self.key_path = key_path

    def _serialize(self, msg: dict) -> bytes:
        return bytes(json.dumps(msg), "ascii")

    def connect(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(self.key_path)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss = ctx.wrap_socket(self.sock, server_hostname=self.host)

        self.ss.connect((self.host, self.port))
        logger.info("socket connect")

    def send(self, msg: dict) -> SrvResp:
        self.s.sendall(self._serialize(dict(msg)))
        resp = self.s.recv(1024)
        logger.debug(f"server response: {resp}")

        if not resp:
            return "remote is offline"
        else:
            return resp

    def close(self):
        self.ss.close()
        logger.info("socket disconnect")


if __name__ == "__main__":
    pass
