import socket
from threading import Thread
from rLog.handler import Handler
from rLog import logger


class Dispatch:
    def __init__(self):
        self.active_handlers = []

    def handle_clients(self):
        host = "0.0.0.0"
        port = 9898

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))

        logger.info("dispatch is online")
        s.listen()

        while True:
            conn, addr = s.accept()
            handler = Handler(conn=conn)
            t = Thread(target=handler.handle_client)
            t.start()
            logger.debug("new handler dispatched")
            self.active_handlers.append(t)

    def shutdown(self):
        for proc in self.active_handlers:
            proc.terminate()
        logger.info("dispatch is offline")


if __name__ == "__main__":
    dispatch = Dispatch()
    try:
        dispatch.handle_clients()

    except Exception as err:
        raise err

    except KeyboardInterrupt:
        pass

    finally:
        dispatch.shutdown()
