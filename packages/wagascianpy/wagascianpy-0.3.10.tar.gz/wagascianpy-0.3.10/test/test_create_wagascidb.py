#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

# pylint: disable=broad-except

"""Unit tests for database creation"""

import os
import shutil
import subprocess
import unittest

import wagascianpy.database.wagascidb
from wagascianpy.utils.utils import silentremove, silentremovedirs
import wagascianpy.utils.environment


class TestCreateWagasciDatabase(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.abspath('.')
        self.test_local_database = os.path.join(self.current_directory, 'test.db')
        self.test_local_simple_repository = os.path.join(self.current_directory, 'test_simple_repo')
        self.test_local_borg_repository = os.path.join(self.current_directory, 'test_borg_repo')
        env = wagascianpy.utils.environment.WagasciEnvironment()
        wagascianpy.database.wagascidb.WagasciDataBase.wagasci_libdir = env["WAGASCI_LIBDIR"]
        self.tearDown()

    def tearDown(self):
        silentremove(self.test_local_database)
        silentremovedirs(self.test_local_borg_repository)

    def test_simple_repo_local_database(self):
        """Create a database locally from a local simple backup repository

        """
        with wagascianpy.database.wagascidb.WagasciDataBase(db_location=self.test_local_database,
                                                            repo_location=self.test_local_simple_repository,
                                                            is_borg_repo=False, update_db=False, rebuild_db=True) as db:
            self.assertEqual(6, len(db.get_all()))

    def test_simple_repo_remote_database(self):
        """Create a database remotely from a local simple backup repository

        """
        with wagascianpy.database.wagascidb.WagasciDataBase(db_location="kekcc:test.db",
                                                            repo_location=self.test_local_simple_repository,
                                                            is_borg_repo=False, update_db=False, rebuild_db=True) as db:
            self.assertEqual(6, len(db.get_all()))

    def test_borg_repo_local_database(self):
        """Create a database locally from a local borg backup repository

        """
        subprocess.call([os.path.join(self.current_directory, "create_test_borg_repo.sh")])

        with wagascianpy.database.wagascidb.WagasciDataBase(db_location=self.test_local_database,
                                                            repo_location=self.test_local_borg_repository,
                                                            is_borg_repo=True, update_db=False, rebuild_db=True) as db:
            self.assertEqual(6, len(db.get_all()))


class TestUpdateWagasciDatabase(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.abspath('.')

        self.test_run_name = "physics_run_2020-01-18_15-12-41_64"
        self.test_local_database = os.path.join(self.current_directory, 'test.db')
        self.test_local_simple_repository = os.path.join(self.current_directory, 'test_simple_repo')
        self.test_local_borg_repository = os.path.join(self.current_directory, 'test_borg_repo')
        self.test_new_run_path = os.path.join(self.current_directory, self.test_run_name)
        self.test_old_run_path = os.path.join(self.test_local_simple_repository, self.test_run_name)

        env = wagascianpy.utils.environment.WagasciEnvironment()
        wagascianpy.database.wagascidb.WagasciDataBase.wagasci_libdir = env["WAGASCI_LIBDIR"]

        silentremovedirs(self.test_new_run_path)
        silentremove(self.test_local_database)
        silentremovedirs(self.test_local_borg_repository)
        shutil.move(self.test_old_run_path, self.test_new_run_path)

        subprocess.call([os.path.join(self.current_directory, "create_test_borg_repo.sh")])

    def tearDown(self):
        silentremove(self.test_local_database)
        silentremovedirs(self.test_local_borg_repository)

    def test_simple_repo_database_update(self):
        """Update a database locally from a local simple backup repository

        """
        with wagascianpy.database.wagascidb.WagasciDataBase(db_location=self.test_local_database,
                                                            repo_location=self.test_local_simple_repository,
                                                            is_borg_repo=False, update_db=False, rebuild_db=True) as db:
            self.assertEqual(5, len(db.get_all()))

        shutil.move(self.test_new_run_path, self.test_old_run_path)

        with wagascianpy.database.wagascidb.WagasciDataBase(db_location=self.test_local_database,
                                                            repo_location=self.test_local_simple_repository,
                                                            is_borg_repo=False, update_db=True, rebuild_db=False) as db:
            self.assertEqual(6, len(db.get_all()))

    def test_borg_repo_database_update(self):
        """Update a database locally from a local borg backup repository

        """
        with wagascianpy.database.wagascidb.WagasciDataBase(db_location=self.test_local_database,
                                                            repo_location=self.test_local_borg_repository,
                                                            is_borg_repo=True, update_db=False, rebuild_db=True) as db:
            self.assertEqual(5, len(db.get_all()))

        shutil.move(self.test_new_run_path, self.test_old_run_path)
        subprocess.call([os.path.join(self.current_directory, "create_test_borg_repo.sh")])

        with wagascianpy.database.wagascidb.WagasciDataBase(db_location=self.test_local_database,
                                                            repo_location=self.test_local_borg_repository,
                                                            is_borg_repo=True, update_db=True, rebuild_db=False) as db:
            self.assertEqual(6, len(db.get_all()))


if __name__ == '__main__':
    unittest.main()
