from socket import socket
from multiprocessing import Process
from rLog import logger
from rLog.models import Message
from rLog.parsers import deserialize
from rLog.settings import csv_evse_pd_cols


class Handler(Process):
    def __init__(self, conn: socket, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.header_exists = False

    def csv_output(self, msg: Message) -> bool:
        csv_out = (f"{msg.timestamp}"
                   f",{msg.device_id}"
                   )
        for col in csv_evse_pd_cols:
            try:
                csv_out += f",{msg.payload[col]}"

            except KeyError as err:
                logger.warning(f"Key not found: {err}")
                return False

        try:
            with open("../csv/test.csv", "a+") as csv:
                if not self.header_exists:
                    header = "timestamp,device_id"
                    for col in csv_evse_pd_cols:
                        header += f",{col}"
                    csv.write(header + "\n")
                    self.header_exists = True
                else:
                    csv.write(csv_out + "\n")

        except Exception as err:
            print(err)
            return False

        return True

    def db_output(self, msg: Message):
        print(f"db: {msg}")

    def run(self):
        logger.info("Handler running")
        while True:
            data = self.conn.recv(1024)
            if not data:
                self.exit()
                break
            else:
                msg = deserialize(data)
                logger.info(msg)

                if "csv" in msg.streams:
                    self.csv_output(msg=msg)

            self.conn.sendall(bytes("ACK", "ascii"))

    def exit(self):
        self.conn.close()
        logger.info(f"client disconnected: {self.addr}")


if __name__ == "__main__":
    pass
