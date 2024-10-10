import os
from queue import Queue
from multiprocessing import Process
from rLog.streams import Stream
from rLog.server import logger
from rLog.server.utils.q_instance import QueueInstance


class QueueManager:
    def __init__(self, stream: Stream):
        self.stream = stream
        self.q = Queue()
        self.active_queues = list()

    def run(self):
        try:
            for stream in self.stream.__subclasses__():
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
