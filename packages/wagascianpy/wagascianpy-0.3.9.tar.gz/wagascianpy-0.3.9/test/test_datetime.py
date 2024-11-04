#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

import unittest
from datetime import datetime
import pytz

from wagascianpy.database.db_record import DBRecord


class TestBsdDatabaseCreation(unittest.TestCase):

    def setUp(self):
        self.expected_dt_string = "2020/01/01 01:01:01"
        self.expected_dt_string_tz = "2020/01/01 01:01:01 JST"
        self.expected_dt = datetime(year=2020, month=1, day=1, hour=1, minute=1, second=1)
        jst = pytz.timezone(DBRecord.get_timezone_str())
        self.expected_dt = jst.localize(self.expected_dt)
        self.expected_timestamp = 1577808061.0

    def test_str2datetime(self):
        dt = DBRecord.str2datetime(self.expected_dt_string)
        self.assertEqual(self.expected_dt, dt)

    def test_tzstr2datetime(self):
        dt = DBRecord.str2datetime(self.expected_dt_string_tz)
        self.assertEqual(self.expected_dt, dt)

    def test_timestamp2datetime(self):
        dt = DBRecord.timestamp2datetime(self.expected_timestamp)
        self.assertEqual(self.expected_dt, dt)

    def test_str2timestamp(self):
        timestamp = DBRecord.str2timestamp(self.expected_dt_string)
        self.assertEqual(self.expected_timestamp, timestamp)

    def test_tzstr2timestamp(self):
        timestamp = DBRecord.str2timestamp(self.expected_dt_string_tz)
        self.assertEqual(self.expected_timestamp, timestamp)

    def test_datetime2timestamp(self):
        timestamp = DBRecord.datetime2timestamp(self.expected_dt)
        self.assertEqual(self.expected_timestamp, timestamp)

    def test_timestamp2str(self):
        dt_string_tz = DBRecord.timestamp2str(self.expected_timestamp)
        self.assertEqual(self.expected_dt_string_tz, dt_string_tz)


if __name__ == '__main__':
    unittest.main()
