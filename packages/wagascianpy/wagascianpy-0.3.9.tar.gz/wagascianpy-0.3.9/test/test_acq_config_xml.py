import unittest

from mock import patch

from wagascianpy.utils.acq_config_xml import *
from wagascianpy.utils.topology import parse_topology_string, gdcc2dif_topology


class TestAcqConfigXml(unittest.TestCase):

    def setUp(self):
        self.acq_config_path = "/test.xml"
        self.topology_str = "full_setup"

    def test_wagasci_config(self):
        wg_config = WagasciConfig(simulate=True)
        self.assertEqual("wg_config", wg_config.module_name)
        self.assertEqual("WG_CONFIG_PORT", wg_config.port_name)
        self.assertIn("wg_config", wg_config.module_id)

    @patch('wagascianpy.utils.acq_config_xml.WagasciConfig')
    def test_create_acq_config_xml(self, mock_wagasci_config):
        conf_string = r'wg_config('
        conf_string += r'topology=%s,' % self.topology_str
        conf_string += r'acq_config_path=%s,' % self.acq_config_path
        conf_string += r'simulate=%s)' % (str(True))
        retcode, res = create_acq_config_xml(topology=self.topology_str, acq_config_path=self.acq_config_path,
                                             simulate=True)
        self.assertEqual(1, retcode)
        self.assertEqual("ok", res)
        mock_wagasci_config.assert_called_once_with(conf_string=conf_string)
        # might fail because of the conf_string ordering but it does not mean that the test failed

    @patch('wagascianpy.utils.acq_config_xml.WagasciConfig')
    def test_create_acq_config_xml_exception(self, mock_wagasci_config):
        mock_wagasci_config.side_effect = RuntimeError("test_exception")
        retcode, res = create_acq_config_xml(topology=self.topology_str, acq_config_path=self.acq_config_path,
                                             simulate=True)
        self.assertEqual(0, retcode)
        self.assertEqual("test_exception", res)


class TestTopology(unittest.TestCase):

    def setUp(self):
        self.wallmrd_south_before = "wallmrd_south"
        self.wallmrd_south_after = '{"1": {"3": {"1": 32, "3": 32, "2": 32}, "4": {"1": 32, "3": 32, "2": 32}}}'
        self.wagasci_downstream_before = "wagasci_downstream"
        self.wagasci_downstream_after = '{"2": {"3": {"11": 32, "10": 32, "13": 32, "12": 32, "15": 32, "14": 32, ' \
                                        '"17": 32, "16": 32, "19": 32, "18": 32, "20": 32, "1": 32, "3": 32, "2": 32, '\
                                        '"5": 32, "4": 32, "7": 32, "6": 32, "9": 32, "8": 32}, "4": {"11": 32, ' \
                                        '"10": 32, "13": 32, "12": 32, "15": 32, "14": 32, "17": 32, "16": 32, ' \
                                        '"19": 32, "18": 32, "20": 32, "1": 32, "3": 32, "2": 32, "5": 32, "4": 32, ' \
                                        '"7": 32, "6": 32, "9": 32, "8": 32}}}'
        self.custom_topology_before = r'{"1": {"3": {"1": 32\, "3": 32\, "2": 32}\, "4": {"1": 32\, "3": 32\, ' \
                                      r'"2": 32}}}'
        self.custom_topology_after = '{"1": {"3": {"1": 32, "3": 32, "2": 32}, "4": {"1": 32, "3": 32, "2": 32}}}'

    def test_topology_parser(self):
        self.assertEqual(self.wallmrd_south_after, parse_topology_string(self.wallmrd_south_before))
        self.assertEqual(self.wagasci_downstream_after, parse_topology_string(self.wagasci_downstream_before))
        self.assertEqual(self.custom_topology_after, parse_topology_string(self.custom_topology_before))

    def test_gdcc2dif_topology_dict(self):
        dif_topology = {"2": {"0": 32, "1": 32, "2": 32}, "3": {"0": 32, "1": 32, "2": 32}}
        self.assertEqual(dif_topology, gdcc2dif_topology(json.loads(self.wallmrd_south_after)))

    def test_gdcc2dif_topology_str(self):
        dif_topology = {"2": {"0": 32, "1": 32, "2": 32}, "3": {"0": 32, "1": 32, "2": 32}}
        self.assertEqual(dif_topology, gdcc2dif_topology(self.wallmrd_south_after))


if __name__ == '__main__':
    unittest.main()
