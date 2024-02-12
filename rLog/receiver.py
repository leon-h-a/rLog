import socket
from rLog.models import Endpoint
from rLog.handlers import Handler
from rLog import logger


class Receiver(Endpoint):
    """
    setup outputs (filepaths, ORMS (+db connect), etc...)
    """
    def __init__(self):
        super().__init__()
        self.clients = 0
        self.handler_processes = list()

    def run_process(self):
        host, port = "0.0.0.0", 9999
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
    asdf = Receiver()
    asdf.run_process()
