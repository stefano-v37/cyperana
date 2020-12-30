import CyPerAna as cpa
import unittest


class InitTest(unittest.TestCase):
    def test_initialization(self):
        inst = cpa.Instance("default")

        self.assertEqual(inst.athlete, "default")
        self.assertEqual(inst.athlete_parameters["cardio-zones-model"], "std-garmin")
        self.assertEqual(inst.wo, {})

    def test_loading(self):
        inst = cpa.Instance("default")
        inst.load("data1.fit")

        self.assertEqual(list(inst.wo.keys()), ["zwift-20201225"])

    def test_multiple_loading(self):
        inst = cpa.Instance("default")
        for i in range(2):
            inst.load("data1.fit")

        self.assertEqual(list(inst.wo.keys()), ["zwift-20201225", "zwift-20201225-1"])

        for i in range(2):
            inst.load("data1.fit")
        self.assertEqual(list(inst.wo.keys()), ["zwift-20201225", "zwift-20201225-1", "zwift-20201225-2",
                                                "zwift-20201225-3"])


if __name__ == '__main__':
    unittest.main()
