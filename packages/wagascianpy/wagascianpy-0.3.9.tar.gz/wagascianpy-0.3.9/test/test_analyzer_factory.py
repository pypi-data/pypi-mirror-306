#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import unittest

import wagascianpy.analysis.analyzer
import wagascianpy.utils.acq_config_xml
import wagascianpy.utils.utils


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.run_root_dir = os.path.abspath('./test_analyzer/physics_run_2020-01-29_18-30-08_92')
        self.bsd_database = os.path.abspath('./test_analyzer/bsddb.db')
        self.bsd_repository = "/media/neo/SDCARD/WAGASCI/BSD"
        self.run_name = 'physics_run_2020-01-29_18-30-08_92'
        self.run_number = 92
        self.save_location = os.path.abspath('./tmp_save')
        self.history_location = os.path.abspath('./tmp_adc_calibration')
        self.sqlite_database = os.path.abspath('../databases/mh_temperature_sensors.sqlite3')
        self.wagasci_xml_config = wagascianpy.utils.acq_config_xml.acqconfigxml_file_finder(
            self.run_root_dir, self.run_name)
        self.chains = {self.run_name: {}}

    def tearDown(self):
        for filename in wagascianpy.utils.utils.find_files(self.run_root_dir, '.root') + \
                        wagascianpy.utils.utils.find_files(self.run_root_dir, '.txt') + \
                        wagascianpy.utils.utils.find_files(self.run_root_dir, '.png'):
            os.remove(filename)
        wagascianpy.utils.utils.silentremovedirs(self.save_location)
        wagascianpy.utils.utils.silentremovedirs(self.history_location)

    def test_decoder(self):
        decoder = wagascianpy.analysis.analyzer.Decoder(run_name=self.run_name,
                                                        run_number=self.run_number,
                                                        run_root_dir=self.run_root_dir,
                                                        output_dir=self.save_location,
                                                        overwrite_flag=True,
                                                        compatibility_mode=False)

        decoder.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)

    def test_adc_distribution(self):
        decoder = wagascianpy.analysis.analyzer.Decoder(run_name=self.run_name,
                                                        run_number=self.run_number,
                                                        run_root_dir=self.run_root_dir,
                                                        output_dir=self.save_location,
                                                        overwrite_flag=True,
                                                        compatibility_mode=False)
        adc = wagascianpy.analysis.analyzer.AdcDistribution(run_name=self.run_name,
                                                            run_number=self.run_number,
                                                            run_root_dir=self.save_location,
                                                            output_dir=self.save_location,
                                                            chip_by_chip=True)
        decoder.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)
        self.chains[self.run_name] = {}
        adc.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)

    def test_spill_number_fixer(self):
        decoder = wagascianpy.analysis.analyzer.Decoder(run_name=self.run_name,
                                                        run_number=self.run_number,
                                                        run_root_dir=self.run_root_dir,
                                                        output_dir=self.save_location,
                                                        overwrite_flag=True,
                                                        compatibility_mode=False)
        spill_fixer = wagascianpy.analysis.analyzer.SpillNumberFixer(run_name=self.run_name,
                                                                     run_root_dir=self.save_location,
                                                                     output_dir=self.save_location)

        decoder.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)
        self.chains[self.run_name] = {}
        spill_fixer.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)

    def test_beam_summary_data(self):
        decoder = wagascianpy.analysis.analyzer.Decoder(run_name=self.run_name,
                                                        run_number=self.run_number,
                                                        run_root_dir=self.run_root_dir,
                                                        output_dir=self.save_location,
                                                        overwrite_flag=True,
                                                        compatibility_mode=False)
        spill_fixer = wagascianpy.analysis.analyzer.SpillNumberFixer(run_name=self.run_name,
                                                                     run_root_dir=self.save_location,
                                                                     output_dir=self.save_location)
        bsd = wagascianpy.analysis.analyzer.BeamSummaryData(run_name=self.run_name,
                                                            run_number=self.run_number,
                                                            run_root_dir=self.save_location,
                                                            output_dir=self.save_location,
                                                            bsd_database=self.bsd_database,
                                                            bsd_repository=self.bsd_repository,
                                                            t2krun=10,
                                                            recursive=True)
        decoder.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)
        self.chains[self.run_name] = {}
        spill_fixer.spawn(self.chains[self.run_name])
        bsd.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)

    def test_adc_calibration(self):
        decoder = wagascianpy.analysis.analyzer.Decoder(run_name=self.run_name,
                                                        run_number=self.run_number,
                                                        run_root_dir=self.run_root_dir,
                                                        output_dir=self.save_location,
                                                        overwrite_flag=True,
                                                        compatibility_mode=False)
        spill_fixer = wagascianpy.analysis.analyzer.SpillNumberFixer(run_name=self.run_name,
                                                                     run_root_dir=self.save_location,
                                                                     output_dir=self.save_location)
        bsd = wagascianpy.analysis.analyzer.BeamSummaryData(run_name=self.run_name,
                                                            run_number=self.run_number,
                                                            run_root_dir=self.save_location,
                                                            output_dir=self.save_location,
                                                            bsd_database=self.bsd_database,
                                                            bsd_repository=self.bsd_repository,
                                                            t2krun=10,
                                                            recursive=True)
        temp = wagascianpy.analysis.analyzer.Temperature(run_name=self.run_name,
                                                         run_number=self.run_number,
                                                         run_root_dir=self.save_location,
                                                         output_dir=self.save_location,
                                                         sqlite_database=self.sqlite_database)
        adc_calibration = wagascianpy.analysis.analyzer.AdcCalibration(run_name="week",
                                                                       run_number=42,
                                                                       run_root_dir=self.save_location,
                                                                       output_dir=self.history_location,
                                                                       topology_source=self.wagasci_xml_config)

        decoder.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)
        self.chains[self.run_name] = {}
        spill_fixer.spawn(self.chains[self.run_name])
        bsd.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)
        self.chains[self.run_name] = {}
        temp.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)
        self.chains["week"] = {}
        adc_calibration.spawn(self.chains["week"])
        wagascianpy.utils.utils.join_chains(self.chains)

    def test_analyzer_factory(self):
        producer = wagascianpy.analysis.analyzer.AnalyzerFactoryProducer()
        factory = producer.get_factory("decoder",
                                       overwrite_flag=True,
                                       compatibility_mode=False)

        decoder = factory.get_analyzer(run_name=self.run_name,
                                       run_number=self.run_number,
                                       run_root_dir=self.run_root_dir,
                                       output_dir=self.save_location)

        decoder.spawn(self.chains[self.run_name])
        wagascianpy.utils.utils.join_chains(self.chains)


if __name__ == '__main__':
    unittest.main()
