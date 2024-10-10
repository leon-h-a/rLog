import csv
from datetime import datetime
from influxdb import InfluxDBClient

from rLog.server.streams import Stream
from rLog.server.utils.responses import Valid, Error

from rLog.server import logger


class CSV(Stream):
    name = "csv"
    port = 8810
    enabled = True

    def setup():
        pass

    def input_sanitize(payload: dict):
        for req in CSV.required_fields:
            if req not in payload.keys():
                return Error(f"field [{req}] not present in payload", False)
        return Valid("Message format accpeted", False)

    def output_generate(payload: dict, db_conn=None):
        dir_base = "/home/master/rlog_telemetry"

        payload["telemetry"]["ts"] = datetime.utcfromtimestamp(
            payload["telemetry"]["ts"]
        ).isoformat() + "Z"

        fn = f"{datetime.now().strftime('%Y-%m-%d')}_{payload['client_id']}"

        with open(
                dir_base + "/" + fn + ".csv", "a+"
                ) as f:
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
    required_fields = Stream.required_fields + ["influx_tag_pair"]
    enabled = True

    def setup() -> InfluxDBClient:
        try:
            # todo: read from config.ini
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

        ts = datetime.utcfromtimestamp(
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
