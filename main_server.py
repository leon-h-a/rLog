import os
import socket
from rLog.remote.handler import Handler
from rLog import logger


class Dispatch:
    """
    setup outputs (filepaths, ORMS (+db connect), etc...)
    """
    def __init__(self):
        super().__init__()
        self.handler_processes = list()

    def run_process(self):
        host, port = os.environ['rLogLocalIP'], int(os.environ['rLogLocalPORT'])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            logger.info(f"Receiver listening {host}:{port}")
            s.bind((host, port))
            s.listen()
            try:
                while True:
                    conn, addr = s.accept()

                    # todo: handle auth

                    handler = Handler(conn=conn, addr=addr)
                    handler.daemon = True
                    self.handler_processes.append(handler)
                    handler.start()

            except Exception as err:
                raise err

            finally:
                self.kill_process()

    def kill_process(self):
        for handler in self.handler_processes:
            handler.terminate()
        logger.info("Receiver graceful exit")


if __name__ == "__main__":
    dispatch = Dispatch()
    dispatch.run_process()
