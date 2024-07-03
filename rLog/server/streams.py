from abc import ABCMeta
from rLog.responses import Error, Valid
from rLog.server import logger


class Stream(metaclass=ABCMeta):
    name: str
    port: None
    required_fields = ["ts", "payload", "client_id"]

    def output_setup():
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

    def output_generate():
        """
        Defines how payload is written to output.
        Used by q_deque.py for writing data to output that was set up in
        output_setup def.
        """
        raise NotImplementedError


class CSV(Stream):
    name = "csv"
    port = 8810
    required_field = Stream.required_fields + ["filepath"]

    def output_setup():
        # make sure directory exists (?)
        pass

    def input_sanitize(payload: dict):
        for req in CSV.required_fields:
            if req not in payload.keys():
                return Error(f"field [{req}] not present in payload", False)

        # todo: sanitize values (ts: int, client_id: str ...)
        pass

        # todo: return response and payload that excludes values needed for
        #       other Streams to reduce memory required for queues
        # note: Stream specific fields are negligible in size compared to
        #       payload size. Stripping might not be needed after all.
        pass

    def output_generate():
        # todo: implement log rotation based on client id
        pass


class Influx(Stream):
    name = "influx"
    port = 8811
    required_fields = Stream.required_fields + ["bucket"]

    def output_setup():
        # influx db connection
        pass

    def input_sanitize(payload: dict):
        pass

    def output_generate():
        pass
