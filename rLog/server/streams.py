import json
from abc import ABCMeta
from rLog.responses import Error, Valid
from rLog.server import logger


class Stream(metaclass=ABCMeta):
    name: str
    port: None

    def __init__(self):
        self.resp = {
            "timestamp": "Field 'timestamp' is not present",
            "streams": "Value 'csv' not present in streams field",
            "payload": "Field 'payload' is not present"
        }

    def _sanitize_required(self, msg: str):
        logger.debug(msg)
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
    port = 8810

    def __init__(self):
        super().__init__()
        # add additional fields that are needed in dequeuer.py
        self.resp["filepath"] = "Field 'filepath' is not present"

    def sanitize(self, msg: str):
        basic_check = self._sanitize_required(msg=msg)
        # Add specific checks
        return basic_check

    def generate(self):
        pass


class Influx(Stream):
    name = "influx"
    port = 8811

    def __init__(self):
        super().__init__()
        # add additional fields that are needed in dequeuer.py
        self.resp["bucket"] = "Field 'bucket' is not present"

    def sanitize(self, msg: str):
        basic_check = self._sanitize_required(msg=msg)
        # Add specific checks
        return basic_check

    def generate(self):
        pass
