import os
import time
import json
import socket
from rLog import logger
from rLog.responses import SrvResp


class Client:
    def __init__(self, client_id: str):
        self.cli_id = client_id
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _serialize(self, msg: dict) -> bytes:
        return bytes(json.dumps(msg), "ascii")

    def connect(self):
        self.s.connect((
            str(os.environ["rLogRemoteIP"]),
            int(os.environ["rLogRemotePORT"])
        ))
        logger.info("socket connect")

    def send(self, msg: dict) -> SrvResp:
        self.s.sendall(self._serialize(dict(msg)))
        resp = self.s.recv(1024)
        logger.debug(f"server response: {resp}")

        if not resp:
            return "Remote is offline"
        else:
            return resp

    def close(self):
        self.s.close()
        logger.info("socket disconnect")


if __name__ == "__main__":
    cli_id = input("Define client id: ")
    cli = Client(cli_id)
    cli.connect()

    try:
        while True:
            resp = cli.send(
                streams=["csv", "psql"],
                payload={
                    "temperature": 12,
                    "humidity": 65,
                    }
                )
            print(f"srv resp: {resp}")
            time.sleep(1)

    except Exception as err:
        raise err

    except KeyboardInterrupt:
        pass

    finally:
        cli.close()
