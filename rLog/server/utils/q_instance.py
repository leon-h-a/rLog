import socket
from multiprocessing import Process, Queue
from logging import Logger
from rLog.server import logger


class QueueInstance:
    def __init__(self):
        self.q = Queue()
        self.handlers = list()
        self.type = None

    def handle_request(
            self,
            q_type: str,
            q_port: int,
            cli: socket,
            q: Queue,
            logger: Logger
            ):

        logger.info(f"[{q_type}] new handler")
        while True:
            try:
                msg = cli.recv(1024)

                if not msg:
                    logger.info(f"[{q_type}] handler disconnected")
                    # determine if disconnect from enque or deque
                    break

                if msg == b'pop':
                    if q.empty():
                        cli.send(bytes("empty", "utf-8"))
                    else:
                        last = q.get()
                        logger.info(f"[{q_type}] dequed: {last}")

                else:
                    q.put(msg)
                    logger.info(f"[{q_type}] enqued: {msg}")
                    cli.send(bytes("ACK", "ascii"))

            except KeyboardInterrupt:
                pass

    def run(self, q_type: str, port: int, logger: Logger):
        self.type = q_type
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("localhost", port))

        logger.info(f"queue [{q_type}] ready on port: {port}")
        s.listen()

        try:
            while True:
                conn, addr = s.accept()
                p = Process(
                    target=self.handle_request,
                    kwargs={
                        "q_type": q_type,
                        "q_port": port,
                        "cli": conn,
                        "q": self.q,
                        "logger": logger
                    }
                )
                self.handlers.append(p)
                p.start()

        except KeyboardInterrupt:
            pass

        except Exception as e:
            raise e

        finally:
            self.shutdown()

    def shutdown(self):
        for proc in self.handlers:
            proc.terminate()
        logger.info(f"queue [{self.type}] shutdown")


if __name__ == "__main__":
    pass
