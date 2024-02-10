import time
import json
import unittest
from rLog.parsers import serialize, deserialize
from rLog.models import Message


class TestParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_serialize(self):
        ts = int(time.time())
        generated = serialize(timestamp=ts, device_id="device_3258", streams=["csv", "db"],
                              temperature=12,
                              humidity=76,
                              state=1
                              )
        expected = bytes(json.dumps(
            dict(
                timestamp=ts,
                device_id="device_3258",
                streams=["csv", "db"],
                payload={'temperature': 12, 'humidity': 76, 'state': 1}
            )
        ), "ascii")
        self.assertEqual(generated, expected)

    def test_deserialize(self):
        ts = int(time.time())
        jsoned = json.dumps(
            dict(
                timestamp=ts,
                device_id="device_3258",
                streams=["csv", "db"],
                payload={'temperature': 12, 'humidity': 76, 'state': 1}
            )
        )
        data = bytes(jsoned, "ascii")
        generated = deserialize(data)
        expected = Message(
            timestamp=ts,
            device_id="device_3258",
            streams=["csv", "db"],
            payload={'temperature': 12, 'humidity': 76, 'state': 1}
        )
        self.assertEqual(generated, expected)

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
