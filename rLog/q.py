import socket
from rLog import logger
from queue import Queue
from threading import Thread


class Queuer:
    def __init__(self):
        self.q = Queue()

    def handle_conn(self, conn: socket):
        try:
            while True:
                msg = conn.recv(1024)
                if not msg:
                    logger.info("Socket disconnected")
                    break

                if msg == b"pop":
                    last = self.q.get()
                    conn.send(last)
                else:
                    self.q.put_nowait(msg)
                    conn.send(bytes("ACK", "ascii"))

            conn.close()

        except ConnectionResetError:
            logger.warning("Handler closed unexpectedly")

    def run_queue(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("localhost", 7777))

        logger.info("Queue online")
        s.listen()

        while True:
            conn, addr = s.accept()
            logger.info("Accepted new connection")
            t = Thread(target=self.handle_conn, args=[conn])
            t.start()


if __name__ == "__main__":
    kvever = Queuer()
    try:
        kvever.run_queue()

    except Exception as err:
        raise err

    except KeyboardInterrupt:
        pass
