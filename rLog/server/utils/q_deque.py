import os
import time
import json
import socket
from multiprocessing import Process
from rLog.streams import Stream
from rLog.server import logger


class DequeueInstance:
    def __init__(self, stream: Stream):
        self.stream = stream
        self.qs = None
        self.db = None
        self.skip_dly = False

    def _output_connect(self):
        self.db = self.stream.setup()

    def _queue_connect(self):
        try:
            self.qs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.qs.connect(("localhost", self.stream.port))
            logger.info(f"connected to [{self.stream.name}] queue")

        except Exception as e:
            raise e

    def _deque_message(self):
        self.qs.send(b"pop")
        data = self.qs.recv(1024)

        if data == b"":
            raise BrokenPipeError

        elif data == b"empty":
            logger.debug(f"[{self.stream.name}] queue is empty")
            return None

        else:
            logger.debug(data)
            return data

    def handle_queue(self):
        while True:
            try:
                self._output_connect()
                self._queue_connect()

                while True:
                    if (data := self._deque_message()):
                        self.stream.output_generate(
                            payload=json.loads(data),
                            db_conn=self.db
                        )
                    else:
                        time.sleep(2)

            except ConnectionRefusedError:
                logger.warning(f"[{self.stream.name}] ConnectionRefusedError")

            except BrokenPipeError:
                logger.warning(f"[{self.stream.name}] BrokenPipeError")

            except ConnectionResetError:
                logger.warning(f"[{self.stream.name}] ConnectionResetError")

            except KeyboardInterrupt:
                self.qs.shutdown(socket.SHUT_RDWR)
                self.qs.close()
                logger.info(f"[{self.stream.name}] disconnected from queue")
                self.stream.output_cleanup(client=self.db)
                logger.info(f"[{self.stream.name}] disconnected from output")
                self.skip_dly = True

            except Exception as e:
                self.qs.shutdown(socket.SHUT_RDWR)
                self.qs.close()
                self.stream.output_cleanup(db_conn=self.db)
                logger.info(f"[{self.stream.name}] disconnected from output")
                logger.error(str(e))
                self.skip_dly = True

            finally:
                if not self.skip_dly:
                    time.sleep(10)


class Dequeuer:
    def __init__(self, stream: Stream):
        self.active_handlers = list()
        self.stream = stream

    def run(self):
        try:
            for stream in self.stream.__subclasses__():
                if stream.port is None:
                    continue
                if not stream.enabled:
                    continue
                dq_instance = DequeueInstance(stream)
                p = Process(
                    target=dq_instance.handle_queue,
                    )
                p.start()
                logger.info(f"[{stream.name}] dequeue proc dispatched")
                self.active_handlers.append(p)

            os.wait()

        except KeyboardInterrupt:
            pass

        except Exception as e:
            raise e

        finally:
            self.shutdown()

    def shutdown(self):
        for proc in self.active_handlers:
            proc.terminate()
        logger.info("dequeue manager shutdown")


if __name__ == "__main__":
    pass
