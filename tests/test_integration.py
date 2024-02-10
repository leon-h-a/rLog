import unittest
from rLog.receiver import Receiver
from rLog.generator import Generator


class TestMessageTransmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_test(self):
        asdf = Receiver()
        asdf.run_process()

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()

