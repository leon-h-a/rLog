import socket
import configparser
from pathlib import Path
from abc import ABCMeta
from datetime import datetime
from influxdb import InfluxDBClient
from rLog.server.utils.responses import Error, Valid
from rLog.server import logger


class Stream(metaclass=ABCMeta):
    name: str
    port: int
    enabled: bool
    q_sock: socket.socket = None
    required_fields = ["ts", "payload", "client_id"]

    def setup():
        """
        Create database connections or system directories.
        """
        raise NotImplementedError

    def input_sanitize(payload: dict) -> [Valid, Error]:
        """
        Checkes if all fields defined for specific stream are present in
        client payload.
        """
        raise NotImplementedError

    def output_generate(payload: dict, out_conn: any):
        """
        Defines how payload is written to storage system.
        """
        raise NotImplementedError

    def output_cleanup():
        """
        Gracefully close existing connections. If they exists.
        """
        raise NotImplementedError


class Influx(Stream):
    name = "influx"
    port = 8811
    q_sock = None
    required_fields = Stream.required_fields + ["influx_tag_pair"]
    enabled = True

    def setup() -> InfluxDBClient:
        cfg = configparser.ConfigParser()
        cfg.read(Path(__file__).parent.parent / "streams.ini")
        cfg = cfg["influx"]
        try:
            return InfluxDBClient(
                host=cfg["host"],
                port=cfg["port"],
                username=cfg["username"],
                password=cfg["password"],
                database=cfg["database"],
                ssl=cfg["ssl"],
                verify_ssl=cfg["verify_ssl"]
            )
            logger.info("influx connected")

        except Exception as e:
            # todo: handle and re-try
            raise e

    def input_sanitize(payload: dict):
        for req in Influx.required_fields:
            if req not in payload.keys():
                return Error(f"field [{req}] not present in payload")
        return Valid("Message format accepted")

    def output_generate(payload: dict, db_conn: InfluxDBClient):
        logger.info(payload)

        ts = datetime.utcfromtimestamp(
            payload["ts"]
        ).isoformat() + "Z"

        output = dict(
            measurement=payload["client_id"],
            tags=payload["influx_tag_pair"],
            time=ts,
            fields=payload["payload"]
        )

        try:
            db_conn.write_points([output])
            logger.info(
                f"[{Influx.name}] {str(payload['client_id'])} write success"
            )

        except Exception as e:
            # todo: add handler
            logger.warning(str(e))
            return Error(str(e))

    def output_cleanup(db_conn: InfluxDBClient):
        db_conn.close()
