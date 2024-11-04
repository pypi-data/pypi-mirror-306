import unittest

import wagascianpy.plotting.parse_args
from wagascianpy.plotting.configuration import fill_configuration, Configuration


class TestParseArgs(unittest.TestCase):

    def setUp(self):
        self.args = [
            '--output-string=buyaka1',
            '--output-path=buyaka2',
            '--wagasci-database=buyaka3',
            '--wagasci-decoded-location=buyaka4',
            '--bsd-database=buyaka5',
            '--bsd-repository=buyaka6',
            '--bsd-download-location=buyaka7',
            '--history-location=buyaka8',
            '--t2krun=10',
            '--start-time=today',
            '--stop-time=tomorrow',
            '--start-run=1',
            '--stop-run=2',
            '--delivered-pot',
            '--accumulated-pot',
            '--bsd-spill-history',
            '--wagasci-spill-history',
            '--wagasci-spill-number',
            '--wagasci-fixed-spill',
            '--temperature',
            '--humidity',
            '--gain-history',
            '--dark-noise-history',
            '--threshold-history',
            '--bcid-history',
            '--all',
            '--run-markers',
            '--maintenance-markers',
            '--trouble-markers',
            '--bsd-markers',
            '--save-tfile',
            '--topology=wagasci_top_downstream',
            '--only-good',
            '--dif=17',
            '--chip=17',
            '--channel=17'
        ]

        self.parsed_args = {
            'output_string': 'buyaka1',
            'output_path': 'buyaka2',
            'wagasci_database': 'buyaka3',
            'wagasci_decoded_location': 'buyaka4',
            'bsd_database': 'buyaka5',
            'bsd_repository': 'buyaka6',
            'bsd_download_location': 'buyaka7',
            'history_location': 'buyaka8',
            't2krun': 10,
            'start_time': 'today',
            'stop_time': 'tomorrow',
            'start_run': 1,
            'stop_run': 2,
            'delivered_pot': True,
            'accumulated_pot': True,
            'bsd_spill_history': True,
            'wagasci_spill_history': True,
            'wagasci_spill_number': True,
            'wagasci_fixed_spill': True,
            'temperature': True,
            'humidity': True,
            'gain_history': True,
            'dark_noise_history': True,
            'threshold_history': True,
            'bcid_history': True,
            'all': True,
            'run_markers': True,
            'maintenance_markers': True,
            'trouble_markers': True,
            'bsd_markers': True,
            'save_tfile': True,
            'topology': 'wagasci_top_downstream',
            'only_good': True,
            'dif': 17,
            'chip': 17,
            'channel': 17
        }

    def test_do_not_crash(self):
        wagascianpy.plotting.parse_args.parse_args(self.args)

    def test_list_flattening(self):
        parsed_args = wagascianpy.plotting.parse_args.parse_args(self.args)
        for name, value in vars(parsed_args).items():
            self.assertNotIsInstance(value, list)

    def test_correct_parsing(self):
        parsed_args = wagascianpy.plotting.parse_args.parse_args(self.args)
        for name, value in self.parsed_args.items():
            print("Testing if argument {} = {}".format(name, value))
            self.assertEqual(value, getattr(parsed_args, name))

    def test_change_configuration(self):
        fill_configuration(self.parsed_args)
        # WAGASCI database configuration
        self.assertEqual(self.parsed_args['wagasci_database'],
                         Configuration.wagascidb.wagasci_database())
        self.assertEqual(self.parsed_args['wagasci_decoded_location'],
                         Configuration.wagascidb.wagasci_decoded_location())
        # BSD database configuration
        self.assertEqual(self.parsed_args['bsd_database'],
                         Configuration.bsddb.bsd_database())
        self.assertEqual(self.parsed_args['bsd_download_location'],
                         Configuration.bsddb.bsd_download_location())
        # global configuration
        self.assertEqual(self.parsed_args['t2krun'],
                         Configuration.global_configuration.t2krun())
        self.assertEqual(self.parsed_args['history_location'],
                         Configuration.global_configuration.history_location())

    def test_parse_topology_by_detector(self):
        topology = wagascianpy.plotting.parse_args.parse_plotting_topology("wagasci_downstream")
        self.assertFalse(topology.are_all_enabled())
        self.assertTrue(topology.wagasci_downstream.is_enabled())
        self.assertFalse(topology.wagasci_upstream.is_enabled())
        self.assertFalse(topology.wallmrd_south.is_enabled())
        self.assertFalse(topology.wallmrd_north.is_enabled())

    def test_parse_topology_by_dif(self):
        topology = wagascianpy.plotting.parse_args.parse_plotting_topology("wagasci_downstream_top,"
                                                                           "wallmrd_south_bottom")
        self.assertFalse(topology.are_all_enabled())
        self.assertTrue(topology.wagasci_downstream_top.is_enabled())
        self.assertTrue(topology.wallmrd_south_bottom.is_enabled())
        self.assertFalse(topology.wagasci_upstream_top.is_enabled())
        self.assertFalse(topology.wallmrd_south_top.is_enabled())
        self.assertFalse(topology.wallmrd_north_top.is_enabled())
        self.assertFalse(topology.wagasci_downstream_side.is_enabled())
        self.assertFalse(topology.wagasci_upstream_side.is_enabled())
        self.assertFalse(topology.wallmrd_north_bottom.is_enabled())


if __name__ == '__main__':
    unittest.main()
