import socket
from threading import Thread
from rLog.handler import Handler
from rLog.server import logger


class ServerBasic:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.active_handlers = []

    def handle_clients(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))

        logger.info("server is online")
        s.listen()

        while True:
            conn, addr = s.accept()
            handler = Handler(conn=conn)
            t = Thread(target=handler.handle_client)
            t.start()
            logger.debug("new handler dispatched")
            self.active_handlers.append(t)

    def shutdown(self):
        for proc in self.active_handlers:
            proc.terminate()
        logger.info("server is offline")


if __name__ == "__main__":
    pass
