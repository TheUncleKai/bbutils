#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

import os
import unittest
import unittest.mock as mock
import sqlite3

from unittest.mock import Mock
from bbutil.database import SQLite, Table, Types
from bbutil.utils import full_path

from bbutil.logging import Logging

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}

crash_error = sqlite3.OperationalError('This did go boing!!')
mock_sub = mock.Mock(side_effect=crash_error)


class TestSQLite(unittest.TestCase):
    """Testing class for locking module."""

    @staticmethod
    def set_log() -> Logging:
        _log = Logging()
        _log.setup(app="Test", level=2, index=_index)

        console = _log.get_writer("console")
        _log.register(console)
        _log.open()
        return _log

    @staticmethod
    def _get_table_01(sqlite_object: SQLite) -> Table:
        _table = Table(name="tester01", sqlite=sqlite_object)
        _table.add_column(name="testid", data_type=Types.integer, unique=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)
        return _table

    def _get_sqlite(self, filename: str, path: str = os.getcwd(), clean: bool = False) -> SQLite:
        _log = self.set_log()
        _testfile = full_path("{0:s}/{1:s}".format(path, filename))
        _name = "Test"

        if (os.path.exists(_testfile) is True) and (clean is True):
            os.remove(_testfile)

        _sqlite = SQLite(filename=_testfile, name="Test", log=_log)
        return _sqlite

    def tearDown(self):
        return

    def test_connect_01(self):
        _log = self.set_log()
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _sqlite = SQLite(filename=_testfile, name="Test", log=_log)

        _check1 = _sqlite.connect()
        _check2 = os.path.exists(_testfile)

        self.assertEqual(_sqlite.name, _name)
        self.assertEqual(_sqlite.filename, _testfile)
        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_sqlite.is_connected)

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)
        return

    def test_connect_02(self):

        _log = self.set_log()
        _name = "Test"

        _sqlite = SQLite(filename="", name="Test", log=_log)

        _check1 = _sqlite.connect()

        self.assertEqual(_sqlite.name, _name)
        self.assertFalse(_check1)
        self.assertFalse(_sqlite.is_connected)
        return

    def test_connect_03(self):

        _log = self.set_log()

        _sqlite = SQLite(filename="", name="", log=_log)

        _check1 = _sqlite.connect()

        self.assertFalse(_check1)
        return

    def test_connect_04(self):

        _log = self.set_log()

        _sqlite = SQLite(filename="", name="Test", log=_log, use_memory=True)

        _check1 = _sqlite.connect()

        self.assertTrue(_check1)
        return

    @mock.patch('sqlite3.connect', new=mock_sub)
    def test_connect_05(self):

        _log = self.set_log()

        _sqlite = SQLite(filename="", name="Test", log=_log, use_memory=True)

        _check1 = _sqlite.connect()

        self.assertFalse(_check1)
        return

    @mock.patch('sqlite3.connect', new=mock_sub)
    def test_connect_06(self):
        _log = self.set_log()
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _sqlite = SQLite(filename=_testfile, name="Test", log=_log)

        _check1 = _sqlite.connect()
        _check2 = os.path.exists(_testfile)

        self.assertEqual(_sqlite.name, _name)
        self.assertEqual(_sqlite.filename, _testfile)
        self.assertFalse(_check1)
        self.assertFalse(_check2)
        return

    def test_connect_07(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _sqlite = SQLite(filename=_testfile, name="Test")

        self.assertRaises(ValueError, _sqlite.connect)
        return

    def test_disconnect_01(self):
        _sqlite = self._get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()
        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        return

    def test_disconnect_02(self):
        _sqlite = self._get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()
        _check2 = _sqlite.disconnect()
        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_disconnect_03(self):
        _sqlite = self._get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()

        _sqlite.commit = True

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        return

    def test_disconnect_04(self):
        _sqlite = self._get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()

        _class_mock = Mock()
        _class_mock.commit = Mock(side_effect=crash_error)

        _sqlite.commit = True
        _sqlite.connection = _class_mock

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        return

    def test_disconnect_05(self):
        _sqlite = self._get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()

        _class_mock = Mock()
        _class_mock.close = Mock(side_effect=crash_error)

        _sqlite.commit = True
        _sqlite.connection = _class_mock

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        return

    def test_check_table_01(self):
        _sqlite = self._get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()
        _check2 = _sqlite.check_table("Test")

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        self.assertTrue(_check3)
        return

    def test_check_table_02(self):
        _sqlite = self._get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _check2 = _sqlite.check_table("tester01")

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_check_table_03(self):
        _sqlite = self._get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=crash_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _check2 = _sqlite.check_table("tester01")

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        self.assertTrue(_check3)
        return

    def test_count_table_01(self):
        _sqlite = self._get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _count = _sqlite.count_table("tester01")

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertEqual(_count, 0)
        self.assertTrue(_check2)
        return

    def test_count_table_02(self):
        _sqlite = self._get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=crash_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _count = _sqlite.count_table("tester01")

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertEqual(_count, -1)
        self.assertTrue(_check2)
        return
