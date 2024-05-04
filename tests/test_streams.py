import unittest
from rLog.streams import CSV, Influx
from rLog.responses import Error, Valid


class TestCSVStream(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csv = CSV()

    def test_missing(self):
        resp = self.csv.sanitize(dict())
        self.assertIsInstance(resp, Error)

    def test_valid(self):
        resp = self.csv.sanitize(
            dict(
                timestamp=123456789,
                streams=["csv"],
                filepath="/home/master/cli_01",
                payload=dict(
                    temperature=12
                )
            )
        )
        self.assertIsInstance(resp, Valid)

    @classmethod
    def tearDownClass(cls):
        pass


class TestInfluxStream(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flux = Influx()

    def test_missing(self):
        resp = self.flux.sanitize(dict())
        self.assertIsInstance(resp, Error)

    def test_valid(self):
        resp = self.flux.sanitize(
            dict(
                timestamp=123456789,
                streams=["flux"],
                bucket="test_bucket",
                payload=dict(
                    temperature=12
                )
            )
        )
        self.assertIsInstance(resp, Valid)
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
