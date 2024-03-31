import os
import socket
from rLog import logger
from rLog.handler import Handler
from multiprocessing import Process


class Dispatch:
    def __init__(self):
        self.active_handlers = []

    def handle_clients(self):
        host = os.environ['rLogLocalIP']
        port = int(os.environ['rLogLocalPORT'])

        logger.info("Dispatch is online")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()

        while True:
            # todo: tls, auth, ddos
            conn, addr = s.accept()
            handler = Handler(conn=conn)
            proc = Process(target=handler.handle_client)
            proc.start()
            self.active_handlers.append(proc)

    def shutdown(self):
        for proc in self.active_handlers:
            proc.terminate()


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
