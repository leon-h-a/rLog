import os
from multiprocessing import Process, Queue
from rLog.server.streams import Stream
from rLog.server import logger
import socket


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
            logger
            ):

        logger.info(f"[{q_type}] new handler")
        while True:
            try:
                msg = cli.recv(1024)

                if not msg:
                    logger.debug(f"[{q_type}] handler disconnected")
                    # determine if disconnect from enque or deque
                    break

                if msg == b'pop':
                    last = q.get()
                    cli.send(last)
                    logger.debug(f"[{q_type}] dequed: {last}")

                else:
                    q.put(msg)
                    logger.debug(f"[{q_type}] enqued: {msg}")
                    cli.send(bytes("ACK", "ascii"))

            except KeyboardInterrupt:
                pass

    def run(self, q_type: str, port: int, logger):
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


class QueueManager:
    def __init__(self):
        self.q = Queue()
        self.active_queues = list()

    def run(self):
        try:
            for stream in Stream.__subclasses__():
                if stream.port is None:
                    continue
                q_instance = QueueInstance()
                p = Process(
                    target=q_instance.run,
                    kwargs={
                            "q_type": stream.name,
                            "port": stream.port,
                            "logger": logger
                        }
                    )
                p.start()
                self.active_queues.append(p)

            os.wait()

        except KeyboardInterrupt:
            pass

        except Exception as e:
            raise e

        finally:
            self.shutdown()

    def shutdown(self):
        for proc in self.active_queues:
            proc.terminate()
        logger.info("queue manager offline")


if __name__ == "__main__":
    pass
