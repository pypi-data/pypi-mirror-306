#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

import os
import unittest

import wagascianpy.database.bsddb
import wagascianpy.utils.utils


class TestBsdDatabaseCreation(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.repository_location = os.path.join(self.current_dir, "test_bsd_repo")
        self.database_location = os.path.join(self.current_dir, "test.db")
        wagascianpy.utils.utils.silentremove(self.database_location)

    def tearDown(self):
        wagascianpy.utils.utils.silentremove(self.database_location)

    def test_local_db_creation(self):
        with wagascianpy.database.bsddb.BsdDataBase(self.database_location, self.repository_location,
                                                    None, 10, False, True) as db:
            self.assertFalse(db.is_fresh_database())

    def test_get_all(self):
        with wagascianpy.database.bsddb.BsdDataBase(self.database_location, self.repository_location,
                                                    None, 10, False, True) as db:
            self.assertEqual(len(db.get_all()), 10)

    def test_pretty_print(self):
        with wagascianpy.database.bsddb.BsdDataBase(self.database_location, self.repository_location,
                                                    None, 10, False, True) as db:
            for record in db.get_all():
                wagascianpy.database.bsddb.BsdRecord(None, record).pretty_print()
                print("")

    def test_get_interval_1(self):
        with wagascianpy.database.bsddb.BsdDataBase(self.database_location, self.repository_location,
                                                    None, 10, False, True) as db:
            # From 1573603898 : Wednesday, November 13, 2019 9:11:38 JST
            # To 1573619355 : Wednesday, November 13, 2019 13:29:15 JST
            for record in db.get_time_interval(1573603898, 1573619355):
                start_time = wagascianpy.database.bsddb.BsdRecord(None, record). \
                    get_start_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
                stop_time = wagascianpy.database.bsddb.BsdRecord(None, record). \
                    get_stop_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
                print("Record name = %s" % record["name"])
                print("Start time  = %s" % start_time)
                print("Stop time   = %s" % stop_time)

    def test_get_interval_2(self):
        with wagascianpy.database.bsddb.BsdDataBase(self.database_location, self.repository_location,
                                                    None, 10, False, True) as db:
            # From 1573603898 : Wednesday, November 13, 2019 9:11:38 JST
            # To 1573606539 : Wednesday, November 13, 2019 9:55:39 JST
            record = db.get_time_interval(1573603898, 1573606539)[0]
            start_time = wagascianpy.database.bsddb.BsdRecord(None, record). \
                get_start_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
            stop_time = wagascianpy.database.bsddb.BsdRecord(None, record). \
                get_stop_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
            self.assertEqual(record["name"], "bsd_run0830152_00v01.root")
            self.assertEqual(start_time, "2019/11/13 09:11:38 JST")
            self.assertEqual(stop_time, "2019/11/13 09:55:39 JST")

    def test_get_interval_3(self):
        with wagascianpy.database.bsddb.BsdDataBase(self.database_location, self.repository_location,
                                                    None, 10, False, True) as db:
            record = db.get_time_interval("2019/11/13 09:11:38 JST", "2019/11/13 09:55:39 JST")[0]
            start_time = wagascianpy.database.bsddb.BsdRecord(None, record). \
                get_start_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
            stop_time = wagascianpy.database.bsddb.BsdRecord(None, record). \
                get_stop_datetime().strftime('%Y/%m/%d %H:%M:%S %Z')
            self.assertEqual(record["name"], "bsd_run0830152_00v01.root")
            self.assertEqual(start_time, "2019/11/13 09:11:38 JST")
            self.assertEqual(stop_time, "2019/11/13 09:55:39 JST")


class TestBsdDatabaseAccess(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.local_repository_location = os.path.join(self.current_dir, 'test_bsd_repo')
        self.local_database_location = os.path.join(self.current_dir, "test.db")
        self.remote_repository_location = 'kekcc:/hsm/nu/wagasci/data/bsd/test'
        self.remote_database_location = 'kekcc:/hsm/nu/wagasci/data/bsd/test/test.db'
        self.download_location = os.path.join(self.current_dir, "test_download")
        wagascianpy.utils.utils.silentremovedirs(self.download_location)
        wagascianpy.utils.utils.silentremove(self.local_database_location)
        wagascianpy.utils.utils.mkdir_p(self.download_location)

    def tearDown(self):
        wagascianpy.utils.utils.silentremove(self.local_database_location)
        wagascianpy.utils.utils.silentremovedirs(self.download_location)

    def test_local_repository(self):
        with wagascianpy.database.bsddb.BsdDataBase(bsd_database_location=self.local_database_location,
                                                    bsd_repository_location=self.local_repository_location,
                                                    bsd_repository_download_location=None,
                                                    t2kruns=10,
                                                    update_db=False,
                                                    rebuild_db=True) as db:
            self.assertEqual(len(db.get_all()), 10)

    def test_remote_repository(self):
        with wagascianpy.database.bsddb.BsdDataBase(bsd_repository_location=self.remote_repository_location,
                                                    bsd_database_location=self.local_database_location,
                                                    bsd_repository_download_location=self.download_location,
                                                    t2kruns=10,
                                                    update_db=False,
                                                    rebuild_db=True) as db:
            self.assertEqual(len(db.get_all()), 10)

    def test_remote_database(self):
        with wagascianpy.database.bsddb.BsdDataBase(bsd_repository_location=self.remote_repository_location,
                                                    bsd_database_location=self.remote_database_location,
                                                    bsd_repository_download_location=self.download_location,
                                                    t2kruns=10,
                                                    update_db=False,
                                                    rebuild_db=True) as db:
            self.assertEqual(len(db.get_all()), 10)


if __name__ == '__main__':
    unittest.main()
