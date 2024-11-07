import unittest
from gate_manager.sweeper import Sweeper
from gate_manager.gate import Gate, GatesGroup
from gate_manager.connection import NanonisSource
from nanonis_tramea import Nanonis


class TestSweeper(unittest.TestCase):
    def setUp(self):
        nanonis_instance = Nanonis()
        source1 = NanonisSource(label="Gate1", read_index=0, write_index=1, nanonisInstance=nanonis_instance)
        source2 = NanonisSource(label="Gate2", read_index=1, write_index=2, nanonisInstance=nanonis_instance)
        self.gate1 = Gate(source=source1)
        self.gate2 = Gate(source=source2)
        self.outputs = GatesGroup(gates=[self.gate1, self.gate2])
        self.sweeper = Sweeper(outputs=self.outputs)

    def test_set_filename(self):
        self.sweeper.temperature = 300
        self.sweeper.comments = "test_sweep"
        self.sweeper.set_x_label(self.outputs)
        self.sweeper.set_y_label(self.gate1)
        self.sweeper.set_filename()
        self.assertIn("300", self.sweeper.filename)
        self.assertIn("test_sweep", self.sweeper.filename)


if __name__ == '__main__':
    unittest.main()
