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

from unittest.mock import Mock
from bbutil.database import SQLite
from bbutil.utils import full_path

from tests.database.helper import (sqlite_crash_error, mock_crash_error, set_log, get_sqlite, get_table_01,
                                   get_data_01, get_data_02)

__all__ = [
    "TestSQLite"
]


class TestSQLite(unittest.TestCase):
    """Testing class for locking module."""

    def tearDown(self):
        return

    def test_connect_01(self):
        _log = set_log()
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

        _log = set_log()
        _name = "Test"

        _sqlite = SQLite(filename="", name="Test", log=_log)

        _check1 = _sqlite.connect()

        self.assertEqual(_sqlite.name, _name)
        self.assertFalse(_check1)
        self.assertFalse(_sqlite.is_connected)
        return

    def test_connect_03(self):

        _log = set_log()

        _sqlite = SQLite(filename="", name="", log=_log)

        _check1 = _sqlite.connect()

        self.assertFalse(_check1)
        return

    def test_connect_04(self):

        _log = set_log()

        _sqlite = SQLite(filename="", name="Test", log=_log, use_memory=True)

        _check1 = _sqlite.connect()

        self.assertTrue(_check1)
        return

    @mock.patch('sqlite3.connect', new=mock_crash_error)
    def test_connect_05(self):

        _log = set_log()

        _sqlite = SQLite(filename="", name="Test", log=_log, use_memory=True)

        _check1 = _sqlite.connect()

        self.assertFalse(_check1)
        return

    @mock.patch('sqlite3.connect', new=mock_crash_error)
    def test_connect_06(self):
        _log = set_log()
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
        _sqlite = get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()
        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        return

    def test_disconnect_02(self):
        _sqlite = get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()
        _check2 = _sqlite.disconnect()
        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_disconnect_03(self):
        _sqlite = get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()

        _sqlite.commit = True

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        return

    def test_disconnect_04(self):
        _sqlite = get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()

        _class_mock = Mock()
        _class_mock.commit = Mock(side_effect=sqlite_crash_error)

        _sqlite.commit = True
        _sqlite.connection = _class_mock

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        return

    def test_disconnect_05(self):
        _sqlite = get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()

        _class_mock = Mock()
        _class_mock.close = Mock(side_effect=sqlite_crash_error)

        _sqlite.commit = True
        _sqlite.connection = _class_mock

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        return

    def test_check_table_01(self):
        _sqlite = get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()
        _check2 = _sqlite.check_table("Test")

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        self.assertTrue(_check3)
        return

    def test_check_table_02(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _check2 = _sqlite.check_table("tester01")

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_check_table_03(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_crash_error)

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
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _count = _sqlite.count_table("tester01")

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertEqual(_count, 0)
        self.assertTrue(_check2)
        return

    def test_count_table_02(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_crash_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _count = _sqlite.count_table("tester01")

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertEqual(_count, -1)
        self.assertTrue(_check2)
        return

    def test_prepare_table_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_prepare_table_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_crash_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        self.assertTrue(_check3)
        return

    def test_prepare_table_03(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_insert_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_01()
        _check3 = _sqlite.insert(_table.name, _table.names, _data)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertTrue(_check4)
        return

    def test_insert_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_02()
        _check3 = _sqlite.insert(_table.name, _table.names, _data)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertTrue(_check4)
        return
