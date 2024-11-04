import unittest

from wagascianpy.pyrmod.pyrmod import PyrameModule, PyrameSlowModule


class TestPyrameModule(unittest.TestCase):

    def setUp(self):
        self.module_name = "test"
        self.module_port = "TEST_PORT"
        self.function1 = "test1"
        self.arguments1 = ["arg1a", "arg1b"]
        self.result1 = (1, "result1")
        self.function0 = "test0"
        self.arguments0 = ["arg0a", "arg0b"]
        self.result0 = (0, "result0")
        self.simulation_dic = {self.function1: self.result1,
                               self.function0: self.result0}
        self.test = PyrameModule(module_name=self.module_name, simulate=True,
                                 simulation_dic=self.simulation_dic)

    def test_constructor(self):
        self.assertEqual(self.module_name, self.test.module_name)
        self.assertEqual(self.module_port, self.test.port_name)
        self.assertTrue(self.test.simulate)
        self.assertDictEqual(self.simulation_dic, self.test.simulation_dic)

    def test_execcmd1(self):
        self.assertEqual(self.result1, self.test.execcmd(self.function1, *self.arguments1))

    def test_execcmd0(self):
        self.assertRaises(RuntimeError, self.test.execcmd, self.function0, *self.arguments0)


class TestSlowModule(unittest.TestCase):

    def setUp(self):
        self.module_name = "test"
        self.module_port = "TEST_PORT"
        self.module_id = "gaaa"
        self.function1 = "test1"
        self.arguments1 = ["arg1a", "arg1b"]
        self.result1 = (1, "result1")
        self.function0 = "test0"
        self.arguments0 = ["arg0a", "arg0b"]
        self.result0 = (0, "result0")
        self.config_str = "a=aaa,b=bbb,c=ccc"
        self.simulation_dic = {self.function1: self.result1,
                               self.function0: self.result0}
        self.test = PyrameSlowModule(module_name=self.module_name,
                                     conf_string=self.config_str,
                                     simulate=True,
                                     simulation_dic=self.simulation_dic)

    def test_constructor(self):
        self.assertEqual(self.module_name, self.test.module_name)
        self.assertEqual(self.module_port, self.test.port_name)
        self.assertTrue(self.test.simulate)
        self.assertIn(self.module_name, self.test.module_id)
        self.assertDictEqual(self.simulation_dic, self.test.simulation_dic)

    def test_execcmd1(self):
        self.assertEqual(self.result1, self.test.execcmd(self.function1, *self.arguments1))

    def test_execcmd0(self):
        self.assertRaises(RuntimeError, self.test.execcmd, self.function0, *self.arguments0)

    def test_fixed_module_id(self):
        test_id = PyrameSlowModule(module_name=self.module_name,
                                   module_id=self.module_id,
                                   conf_string=self.config_str,
                                   simulate=True,
                                   simulation_dic=self.simulation_dic)
        self.assertEqual(self.module_id, test_id.module_id)


if __name__ == '__main__':
    unittest.main()
