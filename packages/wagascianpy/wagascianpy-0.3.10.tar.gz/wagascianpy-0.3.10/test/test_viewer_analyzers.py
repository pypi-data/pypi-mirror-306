import imp
import os
import unittest

from wagascianpy.utils.utils import silentremovedirs
# noinspection PyProtectedMember
from wagascianpy.viewer.configuration import Configuration, RepositoryType, fill_configuration

viewer_module_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', "scripts", "viewer",
                                  "wagasciviewer.py")
wagasciviewer = imp.load_source("wagasciviewer", viewer_module_path)


class TestCheckers(unittest.TestCase):
    def setUp(self):
        fill_configuration()
        self.test_dir = os.path.abspath('../../WagasciAnpy/test')
        databases_dir = os.path.abspath('../../WagasciAnpy/databases')
        Configuration.wagascidb.override({
            'wagasci_database': os.path.join(databases_dir, 'wagascidb.db'),
            'wagasci_repository': os.path.join(self.test_dir, 'test_viewer'),
            'wagasci_download_location': os.path.join(self.test_dir, 'test_viewer'),
            'wagasci_decoded_location': os.path.join(self.test_dir, 'tmp_decoded'),
            'repository_type': RepositoryType.Simple
        })
        Configuration.bsddb.override({
            'bsd_repository': Configuration.bsddb.bsd_repository(),
            'bsd_database': os.path.join(databases_dir, 'bsddb.db'),
            'bsd_download_location': os.path.join(self.test_dir, 'tmp_bsd_download')
        })
        Configuration.global_configuration.override({
            't2krun': 10,
            'history_location': os.path.join(self.test_dir, 'tmp_adc_calibration')
        })
        Configuration.viewer.override({
            'batch_mode': True,
            'update_wagasci_database': False,
            'rebuild_wagasci_database': False,
            'update_bsd_database': False,
            'rebuild_bsd_database': False,
            'wagasci_libdir': None,
            'only_good_runs': False,
            'include_overlapping': False
        })
        Configuration.run_select.override({
            'get_time_interval': False,
            'get_run_interval': False,
            'get_all': False,
            'start_time': None,
            'stop_time': None,
            'start_run': 92,
            'stop_run': 95
        })
        self.app = wagasciviewer.Application(config=Configuration)
        self.app.get_run_interval(start_run=Configuration.run_select.start_run(),
                                  stop_run=Configuration.run_select.stop_run(),
                                  only_good_runs=Configuration.viewer.only_good_runs())

    def tearDown(self):
        silentremovedirs(os.path.join(self.test_dir, 'tmp_bsd_download'))
        silentremovedirs(os.path.join(self.test_dir, 'tmp_decoded'))
        silentremovedirs(os.path.join(self.test_dir, 'tmp_adc_calibration'))

    def decoder(self):
        Configuration.analyzer_configuration.override({
            'decoder': True,
            'overwrite_flag': True
        })
        self.app.analyze(overwrite_flag=Configuration.analyzer_configuration.overwrite_flag())

    def all_but_peu(self):
        Configuration.analyzer_configuration.override({
            'decoder': True,
            'spill_number_fixer': True,
            'beam_summary_data': True,
            'temperature': True,
            'overwrite_flag': True
        })
        self.app.analyze(overwrite_flag=Configuration.analyzer_configuration.overwrite_flag())

    def test_single_multithread_analyzer(self):
        self.decoder()

    def test_single_singlethread_analyzer(self):
        self.decoder()
        Configuration.analyzer_configuration.override({
            'spill_number_fixer': True,
            'overwrite_flag': True
        })
        self.app.analyze(overwrite_flag=Configuration.analyzer_configuration.overwrite_flag())

    def test_multiple_analyzers(self):
        self.all_but_peu()

    def test_single_multirun_analyzer(self):
        self.all_but_peu()
        Configuration.analyzer_configuration.override({
            'adc_calibration': True,
            'overwrite_flag': True
        })
        self.app.analyze(overwrite_flag=Configuration.analyzer_configuration.overwrite_flag())

    def test_multiple_multirun_analyzers(self):
        Configuration.analyzer_configuration.override({
            'all_analyzers': True,
            'overwrite_flag': True
        })
        self.app.analyze(overwrite_flag=Configuration.analyzer_configuration.overwrite_flag())


if __name__ == '__main__':
    unittest.main()
