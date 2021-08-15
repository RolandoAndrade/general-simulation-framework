import unittest

from core.time.simulation_time import SimulationTime, TimeUnit


class TestSimulationTime(unittest.TestCase):
    def test_creation(self):
        """Should create a simulation time"""
        time = SimulationTime(1, TimeUnit.SECOND)
        self.assertEqual(1, time.time)
        self.assertEqual(1000, time.millis)

    def test_add_and_sub(self):
        """Should add and subtract times"""
        time1 = SimulationTime(1, TimeUnit.SECOND)
        time2 = SimulationTime(5, TimeUnit.SECOND)
        time3 = SimulationTime(2, TimeUnit.SECOND)
        self.assertEqual(1, time1.time)
        time4 = time1 + time2
        self.assertEqual(6, time4.time)
        time5 = time4 - time3
        self.assertEqual(4, time5.time)

    def test_convert(self):
        """Should convert units"""
        time_seconds = SimulationTime(60 * 90, TimeUnit.SECOND)
        time_minutes = time_seconds.to_unit(TimeUnit.MINUTE)
        self.assertEqual(90, time_minutes.time)
        time_hours = time_minutes.to_unit(TimeUnit.HOUR)
        self.assertEqual(1.5, time_hours.time)


if __name__ == '__main__':
    unittest.main()
