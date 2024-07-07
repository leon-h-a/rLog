import os
from multiprocessing import Process
from rLog.streams import Stream
from rLog.server import logger
from rLog.server.utils.q_deque import Dequeuer


class DequeueProc:
    def __init__(self):
        self.active_handlers = list()
        pass

    def run(self):
        try:
            for stream in Stream.__subclasses__():
                if stream.port is None:
                    continue
                if not stream.enabled:
                    continue
                dq_instance = Dequeuer(stream)
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
        logger.info("dequeue manager is offline")
