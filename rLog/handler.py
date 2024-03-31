import socket
from rLog import logger


class Handler:
    def __init__(self, conn: socket):
        self.cli_conn = conn
        self.que_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.que_conn.connect(("0.0.0.0", 7777))

    def handle_client(self):
        while True:
            data = self.cli_conn.recv(1024)
            if not data:
                logger.info("Client closed connection")
                break

            else:
                logger.debug(f"Client sent: {data}")

                self.que_conn.send(data)
                q_resp = self.que_conn.recv(1024)
                logger.debug(f"Queue resp: {q_resp}")

                self.cli_conn.sendall(q_resp)


if __name__ == "__main__":
    pass
