import unittest
from gate_manager.connection import NanonisSource, NanonisSourceConnection
from nanonis_tramea import Nanonis


class TestNanonisSource(unittest.TestCase):
    def setUp(self):
        self.nanonis = Nanonis()  # assuming a mock Nanonis instance
        self.source = NanonisSource(label="Test Source", read_index=0, write_index=1, nanonisInstance=self.nanonis)

    def test_attributes(self):
        self.assertEqual(self.source.label, "Test Source")
        self.assertEqual(self.source.read_index, 0)
        self.assertEqual(self.source.write_index, 1)


class TestNanonisSourceConnection(unittest.TestCase):
    def setUp(self):
        self.nanonis = Nanonis()
        self.connection = NanonisSourceConnection(nanonisInstance=self.nanonis)

    def test_connection_outputs(self):
        self.assertEqual(len(self.connection.outputs), 9)
        self.assertIsInstance(self.connection.outputs[1], NanonisSource)
        self.assertEqual(self.connection.outputs[1].label, 'Nanonis output1')


if __name__ == '__main__':
    unittest.main()
