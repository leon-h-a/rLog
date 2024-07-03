import json
import socket
from rLog.server import logger
from rLog.server.streams import Stream
from rLog.responses import Error


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
                for q_conn in self.streams.keys():
                    if (stream := self.streams[q_conn])["q_sock"]:
                        stream["q_sock"].close()
                        logger.info(
                            f"[{self.peer}] queue {q_conn} "
                            f"[{stream['stream_def'].port}] diconnected"
                        )
                break

            payload = json.loads(data)
            print(payload)

            resp = dict()
            # +------------------------------+
            # |   Queue handling             |
            # +------------------------------+
            try:
                if not payload["outputs"]:
                    self.cli_conn.send(Error("Outputs field is empty"))

            except KeyError:
                self.cli_conn.send(Error("No outputs field"))
                # todo: append to response
                continue

            outputs = payload["outputs"]
            for output in outputs:
                if output not in self.streams.keys():
                    self.cli_conn.send(Error("Output not supported"))
                    # todo: append to response
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
                        continue

                    # except Exception as e:
                    #     self.cli_conn.send(Error(str(e)))
                    #     raise e

            # +------------------------------+
            # |   Payload sanitization       |
            # +------------------------------+
            for output in outputs:
                resp[output] = (
                    self.streams[output]["stream_def"].input_sanitize(payload)
                )

            # +------------------------------+
            # |   Enque                      |
            # +------------------------------+
            pass

            # +------------------------------+
            # |   Cumulative response        |
            # +------------------------------+
            # Collect responses from queues and combine them in single
            # response (use dict to json)
            pass

            print(resp)
            self.cli_conn.send(json.dumps(resp).encode("utf8"))


if __name__ == "__main__":
    pass
