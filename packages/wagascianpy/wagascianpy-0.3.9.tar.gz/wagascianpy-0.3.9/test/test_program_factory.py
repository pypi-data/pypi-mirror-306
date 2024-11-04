#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

import os
import unittest

import wagascianpy.program.program
import wagascianpy.utils.utils


class TestProgram(unittest.TestCase):

    def setUp(self):
        self.bsd_database = os.path.abspath('./test_analyzer/bsddb.db')
        self.bsd_repository = '/media/neo/SDCARD/WAGASCI/BSD'
        self.topology_source = os.path.abspath(
            './test_analyzer/physics_run_2020-01-29_18-30-08_92/physics_run_2020-01-29_18-30-08_92.xml')
        self.sqlite_database = os.path.abspath('../databases/mh_temperature_sensors.sqlite3')
        self.history_location = os.path.abspath('./tmp_adc_calibration')

        self.run_dict = {}
        self.save_dict = {}
        self.run_location = './test_analyzer'
        self.save_location = './tmp_save'
        for run_name in os.listdir(self.run_location):
            if os.path.isdir(os.path.join(self.run_location, run_name)):
                self.run_dict[run_name] = os.path.abspath(os.path.join(self.run_location, run_name))
                self.save_dict[run_name] = os.path.abspath(os.path.join(self.save_location, run_name))

    def tearDown(self):
        for run_root_dir in self.run_dict.values():
            for filename in wagascianpy.utils.utils.find_files(run_root_dir, '.root') + \
                            wagascianpy.utils.utils.find_files(run_root_dir, '.txt') + \
                            wagascianpy.utils.utils.find_files(run_root_dir, '.png'):
                os.remove(filename)
        wagascianpy.utils.utils.silentremovedirs(self.save_location)
        wagascianpy.utils.utils.silentremovedirs(self.history_location)

    def test_program(self):
        program = wagascianpy.program.program.Program()
        program.set_run_location(self.run_dict)
        program.set_save_location(self.save_dict)
        program.multiple_runs_analyzer_save_location = self.history_location
        program.do_not_enforce_dependencies()
        program.stop_on_exception()
        program.add_step("decoder", overwrite_flag=True, compatibility_mode=False)
        program.add_step("spill_number_fixer")
        program.add_step("beam_summary_data",
                         bsd_database=self.bsd_database,
                         bsd_repository=self.bsd_repository,
                         t2krun=10,
                         recursive=True)
        program.add_step("temperature", sqlite_database=self.sqlite_database)
        program.add_step("adc_calibration", topology_source=self.topology_source)
        program.start()

    def test_program_builder_dependency(self):
        program = wagascianpy.program.program.Program()
        program.set_run_location(self.run_dict)
        program.set_save_location(self.save_dict)
        program.enforce_dependencies()
        self.assertRaises(RuntimeError, program.add_step, "spill_number_fixer")


if __name__ == '__main__':
    unittest.main()
