import CyPerAna as cpa
import unittest


class InitTest(unittest.TestCase):
    def test_athlete_specific_analyses(self):
        inst = cpa.Instance("default")
        inst.load("data1.fit")

        self.assertEqual(inst.wo['zwift-20201225'].data["cardio_zone"].sum(), 8629)

    def test_non_athlete_specific_analyses(self):
        inst = cpa.Instance("default")
        inst.load("data1.fit")

        self.assertEqual(inst.wo['zwift-20201225'].total_time.total_seconds(), 2711.0)
        self.assertAlmostEqual(inst.wo['zwift-20201225'].data.torque.sum(), 62382.6816679732, 10)
        self.assertAlmostEqual(inst.wo['zwift-20201225'].total_energy, 563757.0, 10)
        self.assertAlmostEqual(inst.wo['zwift-20201225'].fat_burned, 0.015236675675675675, 10)


if __name__ == '__main__':
    unittest.main()
