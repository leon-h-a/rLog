import os
import json
import socket
from abc import ABCMeta
from datetime import datetime
from influxdb import InfluxDBClient
from rLog import logger


class Dequeuer(metaclass=ABCMeta):
    def __init__(self):
        self.q_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.q_sock.connect(("localhost", 7777))
        logger.info("socket connect")

    def _get_value(self):
        self.q_sock.send(b"pop")
        resp = self.q_sock.recv(1024)
        logger.debug(f"dequeue {resp}")
        return resp

    def run_proc(self):
        raise NotImplementedError

    def disconnect(self):
        self.q_sock.close()
        logger.info("socket disconnect")


class CSV(Dequeuer):
    def __init__(self, rotation_interval: int):
        super().__init__()
        self.out_dir = "/home/master/"
        self.d_ref = rotation_interval
        self.d_prev = (ts := datetime.now())  # to trig first log rotate
        self.filename = ts.strftime("%Y%m%dT%H%M%S")

    def _rotate(self):
        d_time = ((ts := datetime.now()) - self.d_prev).total_seconds()
        if d_time > self.d_ref:
            logger.debug("filename rotation")
            self.d_prev = datetime.now()
            self.filename = ts.strftime("%Y%m%dT%H%M%S")

    def run_proc(self):
        try:
            while True:
                self._rotate()

                cli_update = self._get_value()
                recv = json.loads(cli_update.decode("ascii"))

                with open(self.out_dir + self.filename + ".txt", "a+") as f:
                    f.write(json.dumps(recv) + "\n")
                logger.debug(f"write success {self.filename}.txt")

        except Exception as err:
            raise err

        except KeyboardInterrupt:
            pass

        finally:
            self.disconnect()


class Influx(Dequeuer):
    def __init__(self):
        super().__init__()
        self.influx_cli = InfluxDBClient(
            "localhost",
            8086,
            str(os.environ["influxUser"]),
            str(os.environ["influxPass"]),
            str(os.environ["influxBucket"]),
        )

    def run_proc(self):
        try:
            while True:
                cli_update = self._get_value()
                recv = json.loads(cli_update.decode("ascii"))

                influx_pd = dict()
                # influx_pd["measurement"] = recv["table"]  # todo
                influx_pd["measurement"] = "temp"
                influx_pd["time"] = recv["ts"]

                influx_pd["fields"] = dict()
                for k, v in recv["payload"].items():
                    influx_pd["fields"][k] = v

        except Exception as err:
            raise err

        except KeyboardInterrupt:
            pass

        finally:
            self.disconnect()


if __name__ == "__main__":
    asdf = CSV(rotation_interval=5)
    asdf.run_proc()
    # asdf = Influx()
    # asdf.run_proc()
