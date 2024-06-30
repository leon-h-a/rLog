from socket import socket
from rLog.server import logger


class QueueInstance:
    def __init__(self):
        pass

    def handle_conn(self, handler: socket, type: str):
        logger.info(
            f"queue [{type}] listening on port: {socket.getsockname()[1]}"
        )
        try:
            while True:
                msg = handler.recv(1024)
                if not msg:
                    # determine if disconnect from enque or deque
                    break

                if msg == b"pop":
                    last = self.q.get()
                    handler.send(last)
                    logger.debug(f"dequed: {last}")

                else:
                    self.q.put_nowait(msg)
                    logger.debug(f"enqued: {msg}")
                    handler.send(bytes("ACK", "ascii"))

        except ConnectionResetError:
            logger.warning("handler connection closed unexpectedly")

        finally:
            handler.close()

    def run_queue(self):
        # todo: accept connections from clients and dequer and handle r/w
        # if in conf no ip/port, do not boot of if key error
        pass

        # s = socket.socket()
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(("localhost", 7777))

        # logger.info("queue is online")
        # s.listen()

        # try:
        #     while True:
        #         conn, addr = s.accept()
        #         logger.info("handler new connection")
        #         t = Process(target=self.handle_conn, args=[conn])
        #         t.start()

        # except Exception as e:
        #     raise e

        # except KeyboardInterrupt:
        #     self.shutdown()
        #     logger.info("handler disconnected from queue")
