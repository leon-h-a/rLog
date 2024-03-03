import json
from rLog import logger
from socket import socket
from multiprocessing import Process
from json.decoder import JSONDecodeError
from rLog.models import Parser


class Handler(Process):
    def __init__(self, conn: socket, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.available = []
        for i in Parser.__subclasses__(): self.available.append(getattr(i, "identifier"))

    def _check_available(self, streams: list) -> list:
        failed = list()
        for req in streams:
            if req not in self.available:
                failed.append(req)
        return failed

    def run(self):
        logger.info("Handler running")
        while True:
            data = self.conn.recv(1024)
            if not data:
                self.exit()
                break
            else:
                try:
                    payload = json.loads(data)
                    logger.debug(payload)

                    if failed := self._check_available(list(payload["streams"])):
                        logger.warning(f"Requested outputs not supported: {failed}")
                        self.conn.sendall(bytes(f"Requested outputs not supported: {failed}", "ascii"))

                    # todo: parsing per requested module

                    else:
                        self.conn.sendall(bytes("ACK", "ascii"))

                except JSONDecodeError:
                    logger.warning("JSON format error")
                    self.conn.sendall(bytes("JSON format error", "ascii"))

                except Exception as err:
                    self.conn.sendall(bytes(f"{str(err)}", "ascii"))
                    raise err

    def exit(self):
        self.conn.close()
        logger.info(f"Handler shutdown: {self.addr}")


if __name__ == "__main__":
    pass
