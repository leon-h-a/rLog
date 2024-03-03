import time
import socket
from random import randint
from rLog.picklers import serialize
from rLog import logger


class Client:
    def __init__(self, client_id: str):
        super().__init__()
        self.client_id = client_id

    def run_process(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("0.0.0.0", 9999))
            try:
                while True:
                    s.sendall(
                        serialize(
                            timestamp=int(time.time()), device_id=str(self.client_id), streams=["csv", "db"],
                            temperature=randint(-4, 37),
                            humidity=randint(63, 87),
                            state=randint(1, 7)
                        )
                    )
                    resp = s.recv(1024)
                    if not resp:
                        logger.info("Remote is offline")
                        break
                    else:
                        logger.info(f"server resp: {resp}")
                    time.sleep(2)

            except Exception as err:
                raise err

            finally:
                s.close()
                logger.info("Graceful exit")

    def kill_process(self):
        pass


if __name__ == "__main__":
    cli_id = input("generator id: ")
    asdf = Client(cli_id)