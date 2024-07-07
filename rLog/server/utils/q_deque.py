import time
import json
import socket
from rLog.streams import Stream
from rLog.server import logger


class Dequeuer:
    def __init__(self, stream: Stream):
        self.stream = stream
        self.qs = None
        self.db = None

    def _output_connect(self):
        self.db = self.stream.setup()

    def _queue_connect(self):
        while True:
            try:
                self.qs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.qs.connect(("localhost", self.stream.port))
                logger.info(f"[{self.stream.name}] connected to queue")
                break

            except ConnectionRefusedError:
                logger.warning(f"[{self.stream.name}] queue is offline")
                time.sleep(10)

    def _deque_message(self):
        self.qs.send(b"pop")
        data = self.qs.recv(1024)
        if data:
            logger.debug(data)
            return data

    def handle_queue(self):
        while True:
            self._output_connect()
            self._queue_connect()

            try:
                while True:
                    data = self._deque_message()
                    self.stream.output_generate(
                        payload=json.loads(data),
                        db_conn=self.db
                    )

            except KeyboardInterrupt:
                self.qs.shutdown(socket.SHUT_RDWR)
                self.qs.close()
                logger.info(f"[{self.stream.name}] disconnected from queue")
                self.stream.output_cleanup(client=self.db)
                logger.info(f"[{self.stream.name}] disconnected from output")

            except BrokenPipeError:
                logger.warning(f"[{self.stream.name}] queue crashed")
                continue

            except ConnectionResetError:
                logger.warning(f"[{self.stream.name}] queue crashed")
                continue

            except Exception as e:
                self.qs.shutdown(socket.SHUT_RDWR)
                self.qs.close()
                self.stream.output_cleanup(db_conn=self.db)
                logger.info(f"[{self.stream.name}] disconnected from output")
                logger.error(str(e))
                raise e
