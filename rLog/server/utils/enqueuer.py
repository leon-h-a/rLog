import socket
import inspect
from abc import ABCMeta
import rLog.streams as sms
from rLog.streams import Stream
from rLog import logger

classes = inspect.getmembers(sms, inspect.isclass)
streams = [
    cls[1] for cls in classes if not issubclass(cls[1], ABCMeta) and
    cls[1] is not Stream
]


class Enqueuer:
    def __init__(self, conn: socket):
        self.cli_conn = conn
        self.que_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.que_conn.connect(("0.0.0.0", 7777))
        logger.info("enque is online")

    def handle_client(self):
        logger.info("new handler instance running")
        while True:
            data = self.cli_conn.recv(1024)
            if not data:
                logger.info("client closed connection")
                break

            else:
                logger.debug(f"client sent: {data}")

                # todo: parse data as defined in streams.py

                self.que_conn.send(data)
                q_resp = self.que_conn.recv(1024)
                logger.debug(f"queue resp: {q_resp}")

                self.cli_conn.sendall(q_resp)


if __name__ == "__main__":
    pass
