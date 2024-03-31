import os
import time
import socket
from rLog.parsing import serialize
from rLog.models import ServerResponse


class Client:
    def __init__(self, client_id: str):
        self.cli_id = client_id
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((
            str(os.environ["rLogRemoteIP"]),
            int(os.environ["rLogRemotePORT"])
            ))

    def send(self, streams: list, payload: dict) -> ServerResponse:
        self.s.sendall(
            serialize(
                ts=int(time.time()),
                device_id=self.cli_id,
                streams=streams,
                data=payload
                )
            )
        resp = self.s.recv(1024)
        if not resp:
            return ServerResponse("Remote is offline")

        else:
            return ServerResponse(resp)

    def close(self):
        self.s.close()


if __name__ == "__main__":
    cli_id = input("Define client id: ")
    cli = Client(cli_id)

    while True:
        resp = cli.send(
                streams=["csv", "psql"],
                payload={
                    "temperature": 12,
                    "humidity": 65,
                    }
                )
        time.sleep(2)
