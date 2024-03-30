# import os
import time
import socket
from rLog import logger
# from random import randint
from rLog.picklers import serialize


class Client:
    def __init__(self, client_id: str):
        cntr = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((
                "172.104.238.117",
                9898
                ))
            try:
                while True:
                    s.sendall(
                        serialize(
                            ts=int(time.time()), device_id=str(client_id),
                            streams=["csv", "psql"],
                            data=cntr,
                            # temperature=randint(-4, 37),
                            # humidity=randint(63, 87),
                            # state=randint(1, 7)
                        )
                    )
                    cntr += 1
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
    cli_id = input("add client id: ")
    asdf = Client(cli_id)

