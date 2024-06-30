import socket
from multiprocessing import Process
from queue import Queue
from logging import Logger


class QueueInstance:
    def __init__(self):
        self.q = Queue()
        self.handlers = list()
        self.type = None

    def handle_request(self, conn: socket, logger: Logger):
        while True:
            msg = conn.recv(1024)
            if not msg:
                # determine if disconnect from enque or deque
                break

            if msg == b"pop":
                last = self.q.get()
                conn.send(last)
                logger.debug(f"dequed: {last}")

            else:
                self.q.put_nowait(msg)
                logger.debug(f"enqued: {msg}")
                conn.send(bytes("ACK", "ascii"))

    def run(self, type: str, port: int, logger: Logger):
        self.type = type
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("localhost", port))

        logger.info(f"queue [{type}] listening on port: {port}")
        s.listen()

        try:
            while True:
                conn, addr = s.accept()
                logger.info("handler new connection")
                t = Process(
                    target=self.handle_request,
                    kwargs={
                        "conn": conn,
                        "logger": logger
                    }
                )
                self.handlers.append(t)
                t.start()

        except KeyboardInterrupt:
            pass

        except Exception as e:
            raise e

        finally:
            self.shutdown()

    def shutdown(self):
        for proc in self.handlers:
            proc.terminate()
        logger.info(f"queue [{self.type}] offline")


if __name__ == "__main__":
    pass
