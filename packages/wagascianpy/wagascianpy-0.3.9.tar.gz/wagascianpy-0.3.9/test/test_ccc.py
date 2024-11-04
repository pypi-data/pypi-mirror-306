import unittest

from wagascianpy.pyrmod.CCC import CCC


class TestCCC(unittest.TestCase):

    def setUp(self):
        self.spill_period = 100
        self.active_time = 200
        self.simulation_dic = {
            "get_spill_type": (1, "undefined"),
            "get_spill_period": (1, self.spill_period),
            "get_active_time": (1, self.active_time)
        }
        self.ccc = CCC(simulate=True, simulation_dic=self.simulation_dic)

    def test_undefined(self):
        self.ccc.simulation_dic["get_spill_type"] = (1, "undefined")
        self.assertEqual(self.ccc.simulation_dic["get_spill_type"],
                         self.ccc.get_spill_type())

    def test_spill_off(self):
        self.ccc.simulation_dic["get_spill_type"] = (1, "spill off")
        self.ccc.spill_off()
        self.assertEqual(self.ccc.simulation_dic["get_spill_type"],
                         self.ccc.get_spill_type())

    def test_continuous(self):
        self.ccc.simulation_dic["get_spill_type"] = (1, "continuous")
        self.ccc.spill_continuous()
        self.assertEqual(self.ccc.simulation_dic["get_spill_type"],
                         self.ccc.get_spill_type())

    def test_external_spill(self):
        self.ccc.simulation_dic["get_spill_type"] = (1, "external spill")
        self.ccc.spill_external()
        self.assertEqual(self.ccc.simulation_dic["get_spill_type"],
                         self.ccc.get_spill_type())

    def test_internal_spill(self):
        self.ccc.simulation_dic["get_spill_type"] = (1, "internal spill")
        self.ccc.spill_internal()
        self.assertEqual(self.ccc.simulation_dic["get_spill_type"],
                         self.ccc.get_spill_type())
        self.assertEqual(self.ccc.simulation_dic["get_spill_period"],
                         self.ccc.get_spill_period())
        self.assertEqual(self.ccc.simulation_dic["get_active_time"],
                         self.ccc.get_active_time())


if __name__ == '__main__':
    unittest.main()
