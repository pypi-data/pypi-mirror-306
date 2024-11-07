import unittest
from gate import Gate, GatesGroup
from connection import NanonisSource
from nanonis_tramea import Nanonis


class TestGate(unittest.TestCase):
    def setUp(self):
        nanonis_instance = Nanonis()
        source = NanonisSource(label="Test Gate", read_index=0, write_index=1, nanonisInstance=nanonis_instance)
        self.gate = Gate(source=source)

    def test_set_get_voltage(self):
        self.gate.set_volt(1.5)
        self.assertAlmostEqual(self.gate.get_volt(), 1.5, places=1)

    def test_turn_off(self):
        self.gate.set_volt(1.5)
        self.gate.turn_off()
        self.assertAlmostEqual(self.gate.get_volt(), 0.0, places=1)


class TestGatesGroup(unittest.TestCase):
    def setUp(self):
        nanonis_instance = Nanonis()
        source1 = NanonisSource(label="Gate1", read_index=0, write_index=1, nanonisInstance=nanonis_instance)
        source2 = NanonisSource(label="Gate2", read_index=1, write_index=2, nanonisInstance=nanonis_instance)
        self.gate1 = Gate(source=source1)
        self.gate2 = Gate(source=source2)
        self.group = GatesGroup(gates=[self.gate1, self.gate2])

    def test_set_group_voltage(self):
        self.group.set_volt(1.2)
        for gate in self.group.gates:
            self.assertAlmostEqual(gate.get_volt(), 1.2, places=1)


if __name__ == '__main__':
    unittest.main()
