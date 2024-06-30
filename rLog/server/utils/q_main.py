import socket
from queue import Queue
# import inspect
# from abc import ABCMeta
# import rLog.server.streams as sms
from multiprocessing import Process
from rLog.server.streams import Stream
from rLog.server import logger


# classes = inspect.getmembers(sms, inspect.isclass)
# streams = [
#     cls[1] for cls in classes if not issubclass(cls[1], ABCMeta) and
#     cls[1] is not Stream
# ]
print(Stream.__subclasses__())


class QueueManager:
    def __init__(self):
        self.q = Queue()
        print("asdf")

    # def handle_conn(self, handler: socket):
    #     try:
    #         while True:
    #             msg = handler.recv(1024)
    #             if not msg:
    #                 break

    #             if msg == b"pop":
    #                 last = self.q.get()
    #                 handler.send(last)
    #                 logger.debug(f"dequed: {last}")

    #             else:
    #                 self.q.put_nowait(msg)
    #                 logger.debug(f"enqued: {msg}")
    #                 handler.send(bytes("ACK", "ascii"))

    #     except ConnectionResetError:
    #         logger.warning("handler connection closed unexpectedly")

    #     finally:
    #         handler.close()
    #         logger.info("handler disconnected from queue")

    # def run_queue(self):
    #     # if in conf no ip/port, do not boot of if key error
    #     s = socket.socket()
    #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     s.bind(("localhost", 7777))

    #     logger.info("queue is online")
    #     s.listen()

    #     try:
    #         while True:
    #             conn, addr = s.accept()
    #             logger.info("handler new connection")
    #             t = Process(target=self.handle_conn, args=[conn])
    #             t.start()

    #     except Exception as e:
    #         raise e

    #     except KeyboardInterrupt:
    #         self.shutdown()

    def shutdown(self):
        # for proc in self.active_handlers:
        #     proc.terminate()
        logger.info("queue is offline")


if __name__ == "__main__":
    pass
