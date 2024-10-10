import socket
from multiprocessing import Process
from rLog.server.utils.q_enque import Enqueuer
from rLog.server import logger


class ServerBasic:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.active_handlers = []

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))

        logger.info("server is online")
        s.listen()

        try:
            while True:
                conn, addr = s.accept()
                handler = Enqueuer(conn=conn)
                logger.info(f"[{conn.getpeername()[0]}] handler dispatch")
                t = Process(target=handler.handle_client)
                t.start()
                self.active_handlers.append(t)

        except KeyboardInterrupt:
            self.shutdown()

        except Exception as e:
            raise e

        finally:
            self.shutdown()

    def shutdown(self):
        for proc in self.active_handlers:
            proc.terminate()
        logger.info("server is offline")


if __name__ == "__main__":
    pass
