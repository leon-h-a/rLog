import socket
import inspect
from abc import ABCMeta
from rLog import logger
from rLog import Stream
from queue import Queue
from threading import Thread
import rLog.streams as sms


classes = inspect.getmembers(sms, inspect.isclass)
streams = [
    cls[1] for cls in classes if not issubclass(cls[1], ABCMeta) and
    cls[1] is not Stream
]


class Queuer:
    def __init__(self):
        self.q = Queue()

    def handle_conn(self, conn: socket):
        try:
            while True:
                msg = conn.recv(1024)
                if not msg:
                    logger.info("socket disconnected")
                    break

                if msg == b"pop":
                    last = self.q.get()
                    conn.send(last)
                    logger.debug(f"dequed: {last}")

                else:
                    self.q.put_nowait(msg)
                    logger.debug(f"enqued: {msg}")
                    conn.send(bytes("ACK", "ascii"))

        except ConnectionResetError:
            logger.warning("connection closed unexpectedly")

        finally:
            conn.close()
            logger.info("queue is offline")

    def run_queue(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("localhost", 7777))

        logger.info("queue is online")
        s.listen()

        while True:
            conn, addr = s.accept()
            logger.info("accepted new connection")
            t = Thread(target=self.handle_conn, args=[conn])
            t.start()


if __name__ == "__main__":
    # todo: instatiate 1 queue per stream defined
    asdf = Queuer()
    try:
        asdf.run_queue()

    except Exception as err:
        raise err

    except KeyboardInterrupt:
        pass
