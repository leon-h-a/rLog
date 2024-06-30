import os
from queue import Queue
from rLog.server.utils.q_instance import QueueInstance
from multiprocessing import Process
from rLog.server.streams import Stream
from rLog.server import logger


class QueueManager:
    def __init__(self):
        self.q = Queue()
        self.active_queues = list()

        try:
            for stream in Stream.__subclasses__():
                if stream.port is None:
                    continue
                q_instance = QueueInstance()
                t = Process(
                    target=q_instance.run,
                    kwargs={
                            "type": stream.name,
                            "port": stream.port,
                            "logger": logger
                        }
                    )
                t.start()
                logger.info("new handler dispatched")
                self.active_queues.append(t)

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
        logger.info("queue manager is offline")


if __name__ == "__main__":
    pass
