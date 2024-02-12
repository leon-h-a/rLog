import socket
from rLog.models import Endpoint
from rLog.handlers import Handler


class Receiver(Endpoint):
    """
    setup outputs (filepaths, ORMS (+db connect), etc...)
    initialize queue
    spin up receiving endpoint

    graceful exit
    """
    def __init__(self):
        super().__init__()
        self.clients = 0
        self.handler_processes = list()

    def run_process(self):
        HOST, PORT = "0.0.0.0", 9999
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            try:
                while True:
                    conn, addr = s.accept()
                    print("server listening")
                    # todo: handle authorization check
                    handler = Handler(conn=conn, addr=addr)
                    handler.daemon = True
                    self.handler_processes.append(handler)
                    handler.start()

            except Exception as err:
                raise err

            finally:
                for handler in self.handler_processes:
                    handler.terminate()


if __name__ == "__main__":
    asdf = Receiver()
