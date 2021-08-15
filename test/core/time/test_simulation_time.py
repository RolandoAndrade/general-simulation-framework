import unittest

from core.time.simulation_time import SimulationTime, TimeUnit


class TestSimulationTime(unittest.TestCase):
    def test_creation(self):
        time = SimulationTime(1, TimeUnit.SECOND)
        self.assertEqual(1, time.time)
        self.assertEqual(1000, time.millis)

    def test_add_and_sub(self):
        time1 = SimulationTime(1, TimeUnit.SECOND)
        time2 = SimulationTime(5, TimeUnit.SECOND)
        time3 = SimulationTime(2, TimeUnit.SECOND)
        self.assertEqual(1, time1.time)
        time4 = time1 + time2
        self.assertEqual(6, time4.time)
        time5 = time4 - time3
        self.assertEqual(4, time5.time)


if __name__ == '__main__':
    unittest.main()
