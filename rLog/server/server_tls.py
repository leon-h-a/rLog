import ssl
import socket
from threading import Thread
from rLog.handler import Handler
from rLog import logger


class ServerTLS:
    def __init__(self, host: str, port: int, pem_path: str, key_path: str):
        self.host = host
        self.port = port
        self.pem_path = pem_path
        self.key_path = key_path

        self.active_handlers = []

    def handle_clients(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(self.pem_path, self.key_path)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        logger.info("server is online")

        s.listen()
        ss = ctx.wrap_socket(s, server_side=True)

        while True:
            conn, addr = ss.accept()
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
