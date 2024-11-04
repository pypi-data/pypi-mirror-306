#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

# pylint: disable=broad-except

"""Unit tests for database creation"""

import os
import unittest

from wagascianpy.utils.utils import silentremove
import wagascianpy.database.wagascidb


class TestAccessWagasciDatabase(unittest.TestCase):

    def setUp(self):
        self.is_borg_repo = False
        self.update_db = False
        self.rebuild_db = True
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        silentremove(os.path.join(self.current_directory, "test.db"))

    def tearDown(self):
        silentremove(os.path.join(self.current_directory, "test.db"))

    def test_duration(self):
        """Test duration query"""
        with wagascianpy.database.wagascidb.WagasciDataBase(os.path.join(self.current_directory, "test.db"),
                                                            os.path.join(self.current_directory, "test_simple_repo"),
                                                            self.is_borg_repo, self.update_db, self.rebuild_db) as db:
            matched_runs = db.get_duration_greater_than(20)
            self.assertEqual(matched_runs[0]["name"], "physics_run_2020-01-17_15-53-04_63")

    def test_get_time_interval(self):
        """Test time interval query"""
        with wagascianpy.database.wagascidb.WagasciDataBase(os.path.join(self.current_directory, "test.db"),
                                                            os.path.join(self.current_directory, "test_simple_repo"),
                                                            self.is_borg_repo, self.update_db, self.rebuild_db) as db:
            self.assertEqual(db.get_time_interval("2020/01/16 17:00:00", "2020/01/16 23:00:00")[0]["name"],
                             "physics_run_2020-01-16_17-13-41_61")

    def test_get_run_interval(self):
        """Test run interval query"""
        with wagascianpy.database.wagascidb.WagasciDataBase(os.path.join(self.current_directory, "test.db"),
                                                            os.path.join(self.current_directory, "test_simple_repo"),
                                                            self.is_borg_repo, self.update_db, self.rebuild_db) as db:
            self.assertEqual(db.get_run_interval(61, 61)[0]["name"], "physics_run_2020-01-16_17-13-41_61")

    def test_get_all(self):
        """Test get all"""
        with wagascianpy.database.wagascidb.WagasciDataBase(os.path.join(self.current_directory, "test.db"),
                                                            os.path.join(self.current_directory, "test_simple_repo"),
                                                            self.is_borg_repo, self.update_db, self.rebuild_db) as db:
            for record in db.get_all():
                record.pretty_print()
                print("")

    def test_print_run(self):
        """Test pretty printing of run info"""
        with wagascianpy.database.wagascidb.WagasciDataBase(os.path.join(self.current_directory, "test.db"),
                                                            os.path.join(self.current_directory, "test_simple_repo"),
                                                            self.is_borg_repo, self.update_db, self.rebuild_db) as db:
            db.print_run("physics_run_2020-01-17_15-53-04_63")
            print("")

    def test_max_run_number(self):
        """Test getting the maximum run number in the database"""
        with wagascianpy.database.wagascidb.WagasciDataBase(os.path.join(self.current_directory, "test.db"),
                                                            os.path.join(self.current_directory, "test_simple_repo"),
                                                            self.is_borg_repo, self.update_db, self.rebuild_db) as db:
            self.assertEqual(db.get_last_run_number(), 65)


if __name__ == '__main__':
    unittest.main()
