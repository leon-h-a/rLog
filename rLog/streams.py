"""
'message' -> Handler -> Queue -> Poper

Handler:
    * Read which stream the message belongs to
    * Use Stream.sanitize (ack/nack resp)
    * Read Stream.queue (ip:port) and append
        - add static route defs (influx, csv, psql queues)

Poper:
    * Read which stream the message belongs to
    * Use Stream.generate (ORM/SQL) and write to db
    * ? Custom fields for ie csv dir and auto rotation

service.handler:
    * Store all streams to be able to use its sanitize methods -> str

service.poper:
    * Store all streams to be able to use its generate methods -> ORM/SQL
"""
import json
from abc import ABCMeta
from rLog.responses import Error, Valid
from rLog import logger


class Stream(metaclass=ABCMeta):
    name: str

    def __init__(self):
        self.resp = {
            "timestamp": "Field 'timestamp' is not present",
            "streams": "Value 'csv' not present in streams field",
            "payload": "Field 'payload' is not present"
        }

    def _sanitize_required(self, msg: str):
        try:
            json.loads(str(msg).replace("'", '"'))
            for key in self.resp.keys():
                msg[key]

        except KeyError as e:
            return Error(text=self.resp[e.args[0]])

        except Exception as e:
            raise e
            return Error(text=str(e))

        return Valid(text="Message passed to queue")

    def sanitize(self, msg: str):
        """
        check data validity and respond with ACK/NACK
        """
        raise NotImplementedError

    def generate(self):
        """
        generate object ready for storage
        """
        raise NotImplementedError


class CSV(Stream):
    name = "csv"

    def __init__(self):
        super().__init__()
        # add additional fields that are needed in dequeuer.py
        self.resp["filepath"] = "Field 'filepath' is not present"

    def sanitize(self, msg: str):
        basic_check = self._sanitize_required(msg=msg)
        # Implement optional checks
        return basic_check

    def generate(self):
        pass


class Influx(Stream):
    name = "influx"

    def __init__(self):
        super().__init__()
        # add additional fields that are needed in dequeuer.py
        self.resp["bucket"] = "Field 'bucket' is not present"

    def sanitize(self, msg: str):
        basic_check = self._sanitize_required(msg=msg)
        # Implement optional checks
        return basic_check

    def generate(self):
        pass
