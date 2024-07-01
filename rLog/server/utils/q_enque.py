import json
import socket
from rLog.server import logger
from rLog.server.streams import Stream
from rLog.responses import Valid, Error


class Enqueuer:
    def __init__(self, conn: socket):
        self.cli_conn = conn
        self.peer = conn.getpeername()[0]

        self.streams = dict()
        for stream in Stream.__subclasses__():
            self.streams[stream.name] = dict(
                stream_def=stream,
                q_sock=None
            )

    def handle_client(self):
        logger.info(f"[{self.peer}] handler running")
        while True:
            data = self.cli_conn.recv(1024)
            if not data:
                logger.info(f"[{self.peer}] client diconnected")
                # todo: break queue connections before exiting
                break

            payload = json.loads(data)
            print(payload)

            # +------------------------------+
            # |   Queue handling             |
            # +------------------------------+
            try:
                if not payload["outputs"]:
                    self.cli_conn.send(Error("Outputs field is empty"))

            except KeyError:
                self.cli_conn.send(Error("No outputs field"))

            outputs = payload["outputs"]
            for output in outputs:
                if output not in self.streams.keys():
                    self.cli_conn.send(Error("Output not supported"))
                    continue
                else:
                    stream = self.streams[output]

                q_sock = stream["q_sock"]
                if q_sock is None:
                    try:
                        q_sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM
                        )
                        q_sock.connect((
                            "localhost", stream["stream_def"].port
                        ))
                        self.streams[output]["q_sock"] = q_sock

                    except ConnectionRefusedError:
                        self.cli_conn.send(Error("Queue offline"))

                    except Exception as e:
                        raise e

            self.cli_conn.send(Valid("Good msg"))

            # +------------------------------+
            # |   Message sanitization       |
            # +------------------------------+
            # todo: parse data by using streams.py
            pass

            # +------------------------------+
            # |   Enque                      |
            # +------------------------------+
            pass


if __name__ == "__main__":
    pass
