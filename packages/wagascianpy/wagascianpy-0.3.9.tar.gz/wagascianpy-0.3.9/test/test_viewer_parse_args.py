import unittest

# noinspection PyProtectedMember
import wagascianpy.viewer.parse_args
# noinspection PyProtectedMember
from wagascianpy.viewer.configuration import fill_configuration, Configuration, RepositoryType


class TestParseArgs(unittest.TestCase):

    def setUp(self):
        self.args = [
            '--batch-mode',
            '--wagasci-repository=buyaka1',
            '--simple-wagasci-repository',
            '--borg-wagasci-repository',
            '--update-wagasci-database',
            '--rebuild-wagasci-database',
            '--wagasci-database=buyaka2',
            '--wagasci-libdir=buyaka3',
            '--bsd-repository=buyaka4',
            '--bsd-database=buyaka5',
            '--bsd-download-location=buyaka6',
            '--update-bsd-database',
            '--rebuild-bsd-database',
            '--wagasci-download-location=buyaka7',
            '--wagasci-decoded-location=buyaka8',
            '--temperature-sqlite-database=buyaka9',
            '--history-location=buyaka10',
            '--t2krun=10',
            '--start-time=today',
            '--stop-time=tomorrow',
            '--start-run=1',
            '--stop-run=2',
            '--only-good-runs',
            '--include-overlapping',
            '--download',
            '--decoder',
            '--bcid-distribution',
            '--adc-distribution',
            '--spill-number-fixer',
            '--beam-summary-data',
            '--adc-calibration',
            '--temperature',
            '--all-analyzers',
            '--overwrite-flag'
        ]

        self.parsed_args = {
            'batch_mode': True,
            'wagasci_repository': 'buyaka1',
            'simple_wagasci_repository': True,
            'borg_wagasci_repository': True,
            'update_wagasci_database': True,
            'rebuild_wagasci_database': True,
            'wagasci_database': 'buyaka2',
            'wagasci_libdir': 'buyaka3',
            'bsd_repository': 'buyaka4',
            'bsd_database': 'buyaka5',
            'bsd_download_location': 'buyaka6',
            'update_bsd_database': True,
            'rebuild_bsd_database': True,
            'wagasci_download_location': 'buyaka7',
            'wagasci_decoded_location': 'buyaka8',
            'temperature_sqlite_database': 'buyaka9',
            'history_location': 'buyaka10',
            't2krun': 10,
            'start_time': 'today',
            'stop_time': 'tomorrow',
            'start_run': 1,
            'stop_run': 2,
            'only_good_runs': True,
            'include_overlapping': True,
            'download': True,
            'decoder': True,
            'bcid_distribution': True,
            'adc_distribution': True,
            'spill_number_fixer': True,
            'beam_summary_data': True,
            'adc_calibration': True,
            'temperature': True,
            'all_analyzers': True,
            'overwrite_flag': True
        }

    def test_do_not_crash(self):
        wagascianpy.viewer.parse_args.parse_args(self.args)

    def test_list_flattening(self):
        parsed_args = wagascianpy.viewer.parse_args.parse_args(self.args)
        for name, value in vars(parsed_args).items():
            self.assertNotIsInstance(value, list)

    def test_correct_parsing(self):
        parsed_args = wagascianpy.viewer.parse_args.parse_args(self.args)
        for name, value in self.parsed_args.items():
            self.assertEqual(value, getattr(parsed_args, name))

    def test_get_time_interval_configuration(self):
        self.parsed_args['batch_mode'] = True
        self.parsed_args['start_run'] = 0
        self.parsed_args['stop_run'] = 0
        self.parsed_args['start_time'] = 'today'
        self.parsed_args['stop_time'] = 'tomorrow'
        self.parsed_args['borg_wagasci_repository'] = False
        fill_configuration(self.parsed_args)
        self.assertEqual(self.parsed_args['start_time'], Configuration.run_select.start_time())
        self.assertEqual(self.parsed_args['stop_time'], Configuration.run_select.stop_time())
        self.assertEqual(self.parsed_args['start_run'], Configuration.run_select.start_run())
        self.assertEqual(self.parsed_args['stop_run'], Configuration.run_select.stop_run())
        self.assertTrue(Configuration.run_select.get_time_interval())
        self.assertFalse(Configuration.run_select.get_run_interval())
        self.assertFalse(Configuration.run_select.get_all())

    def test_get_run_interval_configuration(self):
        self.parsed_args['batch_mode'] = True
        self.parsed_args['start_run'] = 1
        self.parsed_args['stop_run'] = 10
        self.parsed_args['start_time'] = None
        self.parsed_args['stop_time'] = None
        self.parsed_args['borg_wagasci_repository'] = False
        fill_configuration(self.parsed_args)
        self.assertEqual(self.parsed_args['start_time'], Configuration.run_select.start_time())
        self.assertEqual(self.parsed_args['stop_time'], Configuration.run_select.stop_time())
        self.assertEqual(self.parsed_args['start_run'], Configuration.run_select.start_run())
        self.assertEqual(self.parsed_args['stop_run'], Configuration.run_select.stop_run())
        self.assertFalse(Configuration.run_select.get_time_interval())
        self.assertTrue(Configuration.run_select.get_run_interval())
        self.assertFalse(Configuration.run_select.get_all())

    def test_get_all_configuration(self):
        self.parsed_args['batch_mode'] = True
        self.parsed_args['start_run'] = 0
        self.parsed_args['stop_run'] = 0
        self.parsed_args['start_time'] = None
        self.parsed_args['stop_time'] = None
        self.parsed_args['borg_wagasci_repository'] = False
        fill_configuration(self.parsed_args)
        self.assertEqual(self.parsed_args['start_time'], Configuration.run_select.start_time())
        self.assertEqual(self.parsed_args['stop_time'], Configuration.run_select.stop_time())
        self.assertEqual(self.parsed_args['start_run'], Configuration.run_select.start_run())
        self.assertEqual(self.parsed_args['stop_run'], Configuration.run_select.stop_run())
        self.assertFalse(Configuration.run_select.get_time_interval())
        self.assertFalse(Configuration.run_select.get_run_interval())
        self.assertTrue(Configuration.run_select.get_all())

    def test_change_configuration(self):
        self.parsed_args['batch_mode'] = True
        self.parsed_args['borg_wagasci_repository'] = False
        self.parsed_args['simple_wagasci_repository'] = True
        fill_configuration(self.parsed_args)
        # WAGASCI database configuration
        self.assertEqual(self.parsed_args['wagasci_database'],
                         Configuration.wagascidb.wagasci_database())
        self.assertEqual(self.parsed_args['wagasci_repository'],
                         Configuration.wagascidb.wagasci_repository())
        self.assertEqual(self.parsed_args['wagasci_download_location'],
                         Configuration.wagascidb.wagasci_download_location())
        self.assertEqual(self.parsed_args['wagasci_decoded_location'],
                         Configuration.wagascidb.wagasci_decoded_location())
        self.assertEqual(RepositoryType.Simple,
                         Configuration.wagascidb.repository_type())
        # BSD database configuration
        self.assertEqual(self.parsed_args['bsd_repository'],
                         Configuration.bsddb.bsd_repository())
        self.assertEqual(self.parsed_args['bsd_database'],
                         Configuration.bsddb.bsd_database())
        self.assertEqual(self.parsed_args['bsd_download_location'],
                         Configuration.bsddb.bsd_download_location())
        # global configuration
        self.assertEqual(self.parsed_args['t2krun'],
                         Configuration.global_configuration.t2krun())
        self.assertEqual(self.parsed_args['history_location'],
                         Configuration.global_configuration.history_location())
        # temperature configuration
        self.assertEqual(self.parsed_args['temperature_sqlite_database'],
                         Configuration.temperature.temperature_sqlite_database())

    def test_repository_type(self):
        self.parsed_args['borg_wagasci_repository'] = True
        self.parsed_args['simple_wagasci_repository'] = False
        fill_configuration(self.parsed_args)
        self.assertEqual(RepositoryType.Borg,
                         Configuration.wagascidb.repository_type())


if __name__ == '__main__':
    unittest.main()
