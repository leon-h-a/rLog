from rLog import logger
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

from abc import ABCMeta


class Stream(metaclass=ABCMeta):
    name: str

    def sanitize():
        """
        check data validity and respond with ACK/NACK
        """
        raise NotImplementedError

    def generate():
        """
        generate object ready for storage
        """
        raise NotImplementedError


class CSV(Stream):
    name = "csv"

    def sanitize(self):
        pass

    def generate():
        pass


class Influx(Stream):
    name = "influx"

    def sanitize(self):
        pass

    def generate(self):
        pass
