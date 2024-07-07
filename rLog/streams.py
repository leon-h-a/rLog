import csv
import socket
import datetime
from abc import ABCMeta
from influxdb import InfluxDBClient
from rLog.server import logger
from rLog.server.responses import Error, Valid


class Stream(metaclass=ABCMeta):
    name: str
    port: int
    q_sock: socket.socket
    enabled: bool
    required_fields = ["ts", "payload", "client_id"]

    def setup():
        """
        Execute output setup (ie. dir setup, db connection...).
        """
        raise NotImplementedError

    def input_sanitize(payload: dict) -> [Valid, Error]:
        """
        Defines what fields for specific streams are required.
        Used by q_enque.py to sanitize and push to queue.
        """
        raise NotImplementedError

    def output_generate(payload: dict, out_conn: any):
        """
        Defines how payload is written to output.
        Used by q_deque.py for writing data to output that was set up in
        output_setup def.
        """
        raise NotImplementedError

    def output_cleanup():
        """
        Gracefully exit existing connections.
        """
        raise NotImplementedError


class CSV(Stream):
    name = "csv"
    port = 8810
    q_sock = None
    enabled = True
    required_field = Stream.required_fields + ["filename"]

    def setup():
        pass

    def input_sanitize(payload: dict):
        for req in CSV.required_fields:
            if req not in payload.keys():
                return Error(f"field [{req}] not present in payload", False)
        return Valid("Message format accpeted", False)

    def output_generate(payload: dict, db_conn=None):
        dir_base = "/home/master/rlog_telemetry"

        payload["telemetry"]["ts"] = datetime.datetime.utcfromtimestamp(
            payload["telemetry"]["ts"]
        ).isoformat() + "Z"

        with open(dir_base + "/" + payload["filename"] + ".csv", "a+") as f:
            w = csv.writer(f)
            f.seek(0)
            if len(f.readlines()) == 0:
                w.writerow(payload["telemetry"])
            w.writerow(payload["telemetry"].values())

        logger.info(
            f"[{CSV.name}] {str(payload['client_id'])} write success"
        )

    def output_cleanup(**empty):
        pass


class Influx(Stream):
    name = "influx"
    port = 8811
    q_sock = None
    required_fields = Stream.required_fields + ["influx_tag_pair"]
    enabled = True

    def setup() -> InfluxDBClient:
        try:
            return InfluxDBClient(
                host='localhost',
                port=8086,
                username='master',
                password='master',
                database='test',
                ssl=False,
                verify_ssl=False
            )
            logger.info("influx connected")

        except Exception as e:
            # todo: handle and re-try
            raise e

    def input_sanitize(payload: dict):
        for req in Influx.required_fields:
            if req not in payload.keys():
                return Error(f"field [{req}] not present in payload", False)
        return Valid("Message format accepted", False)

    def output_generate(payload: dict, db_conn: InfluxDBClient):
        logger.debug(payload)

        ts = datetime.datetime.utcfromtimestamp(
            payload["telemetry"]["ts"]
        ).isoformat() + "Z"

        output = dict(
            measurement=payload["client_id"],
            tags=payload["influx_tag_pair"],
            time=ts,
            fields=payload["telemetry"]
        )

        try:
            db_conn.write_points([output])
            logger.info(
                f"[{Influx.name}] {str(payload['client_id'])} write success"
            )

        except Exception as e:
            # todo: add handler
            raise e

    def output_cleanup(db_conn: InfluxDBClient):
        db_conn.close()
