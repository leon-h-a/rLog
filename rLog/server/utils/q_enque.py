import json
import socket
from rLog.server import logger
from rLog.server.streams import Stream
from rLog.server.utils.responses import Valid, Error


class Enqueuer:
    def __init__(self, conn: socket):
        self.cli_conn = conn
        self.peer = conn.getpeername()[0]

        self.streams = dict()
        for stream in Stream.__subclasses__():
            self.streams[stream.name] = dict(
                stream=stream,
                q_sock=None
            )

    def handle_client(self):
        logger.info(f"[{self.peer}] handler running")

        while True:
            data = self.cli_conn.recv(1024)
            if not data:
                logger.info(f"[{self.peer}] client disconnected")
                for q_conn in self.streams.keys():
                    if (stream := self.streams[q_conn])["q_sock"]:
                        stream["q_sock"].shutdown(socket.SHUT_RDWR)
                        stream["q_sock"].close()
                        logger.info(
                            f"[{self.peer}] queue {q_conn} "
                            f"[{stream['stream'].port}] disconnected"
                        )
                break

            payload = json.loads(data)
            resp = dict()
            try:
                if not payload["streams"]:
                    self.cli_conn.send(Error("Streams field is empty").to_bytes())

            except KeyError:
                self.cli_conn.send(Error("No streams field").to_bytes())
                continue

            outputs = payload["streams"]
            for output in outputs:
                if output not in self.streams.keys():
                    resp[output] = Error("Stream not supported")
                    continue
                if not self.streams[output]["stream"].enabled:
                    resp[output] = Error("Stream disabled on remote")
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
                            "localhost", stream["stream"].port
                        ))
                        self.streams[output]["q_sock"] = q_sock

                    except ConnectionRefusedError:
                        resp[output] = Error("Queue offline")
                        continue

                    except Exception as e:
                        resp[output] = Error(str(e))
                        raise e

                sanitize = (
                    self.streams[output]["stream"].input_sanitize(payload)
                )

                if isinstance(sanitize, Error):
                    resp[output] = sanitize

                else:
                    try:
                        self.streams[output]["q_sock"].send(bytes(
                            json.dumps(payload), "ascii"
                            )
                        )
                        resp[output] = Valid("Message enqued")

                    except Exception as e:
                        resp[output] = Error(str(e))

                resp[output] = resp[output].to_json()

            self.cli_conn.send(json.dumps(resp).encode("ascii"))


if __name__ == "__main__":
    pass
