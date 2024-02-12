import time
import socket
from random import randint
from rLog.models import Endpoint
from rLog.parsers import serialize
from rLog import logger


class Generator(Endpoint):
    def __init__(self, client_id: str):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("0.0.0.0", 9999))
            # s.connect(("192.168.1.107", 9999))
            try:
                while True:
                    s.sendall(
                        serialize(
                            timestamp=int(time.time()), device_id=str(client_id), streams=["csv", "db"],
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

    def run_process(self):
        pass

    def kill_process(self):
        pass


if __name__ == "__main__":
    cli_id = input("generator id: ")
    asdf = Generator(cli_id)
