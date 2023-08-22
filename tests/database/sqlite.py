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

from tests.helper.sqlite import (sqlite_operational_error, sqlite_integrity_error, sqlite_unknown_error,
                                 mock_operational_error, get_table_01, get_data_01,
                                 get_data_02, get_data_03, get_data_04, get_data_05, get_data_06, get_data_07,
                                 get_data_08)

from tests.helper import get_sqlite, set_log

__all__ = [
    "TestSQLite"
]


class TestSQLite(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_connect_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _sqlite = SQLite(filename=_testfile, name="Test")

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
        _name = "Test"
        _sqlite = SQLite(filename="", name="Test")

        _check1 = _sqlite.connect()

        self.assertEqual(_sqlite.name, _name)
        self.assertFalse(_check1)
        self.assertFalse(_sqlite.is_connected)
        return

    def test_connect_03(self):
        _sqlite = SQLite(filename="", name="")

        _check1 = _sqlite.connect()

        self.assertFalse(_check1)
        return

    def test_connect_04(self):
        _sqlite = SQLite(filename="", name="Test", use_memory=True)

        _check1 = _sqlite.connect()

        self.assertTrue(_check1)
        return

    @mock.patch('sqlite3.connect', new=mock_operational_error)
    def test_connect_05(self):
        _sqlite = SQLite(filename="", name="Test", use_memory=True)

        _check1 = _sqlite.connect()

        self.assertFalse(_check1)
        return

    @mock.patch('sqlite3.connect', new=mock_operational_error)
    def test_connect_06(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _sqlite = SQLite(filename=_testfile, name="Test")

        _check1 = _sqlite.connect()
        _check2 = os.path.exists(_testfile)

        self.assertEqual(_sqlite.name, _name)
        self.assertEqual(_sqlite.filename, _testfile)
        self.assertFalse(_check1)
        self.assertFalse(_check2)
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
        _class_mock.commit = Mock(side_effect=sqlite_operational_error)

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
        _class_mock.close = Mock(side_effect=sqlite_operational_error)

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
        _cursor_mock.execute = Mock(side_effect=sqlite_operational_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _check2 = _sqlite.check_table("tester01")

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        self.assertTrue(_check3)
        return

    def test_check_table_04(self):
        _sqlite = get_sqlite(filename="test.sqlite")

        _check1 = _sqlite.connect()

        _sqlite.connection = None

        _check2 = _sqlite.check_table("Test")

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
        _cursor_mock.execute = Mock(side_effect=sqlite_operational_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _count = _sqlite.count_table("tester01")

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertEqual(_count, -1)
        self.assertTrue(_check2)
        return

    def test_count_table_03(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")

        _check1 = _sqlite.connect()
        _sqlite.connection = None

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
        _cursor_mock.execute = Mock(side_effect=sqlite_operational_error)

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

    def test_prepare_table_04(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()
        _sqlite.connection = None

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        self.assertTrue(_check3)
        return

    def test_insert_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_01()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, 1)
        self.assertTrue(_check3)
        return

    def test_insert_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_02()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, -1)
        self.assertTrue(_check3)
        return

    def test_insert_03(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_integrity_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _data = get_data_01()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, -1)
        self.assertTrue(_check3)
        return

    def test_insert_04(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_unknown_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _data = get_data_01()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, -1)
        self.assertTrue(_check3)
        return

    def test_insert_05(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_03()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, -1)
        self.assertTrue(_check4)
        return

    def test_insert_06(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_04()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, -1)
        self.assertTrue(_check3)
        return

    def test_insert_07(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_05()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, 6)
        self.assertTrue(_check3)
        return

    def test_insert_08(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_05()
        _sqlite.connection = None

        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, -1)
        self.assertTrue(_check3)
        return

    def test_insert_09(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_06()
        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertEqual(count, -1)
        self.assertTrue(_check3)
        return

    def test_update_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_05()
        _new = get_data_07()
        sql_filter = "testid = ?"

        count = _sqlite.insert(_table.name, _table.names, _data)
        _check3 = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertEqual(count, 6)
        self.assertTrue(_check4)
        return

    def test_update_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_05()
        _new = get_data_07()
        sql_filter = "testid = ?"

        count = _sqlite.insert(_table.name, _table.names, _data)
        _sqlite.connection = None
        _check3 = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertEqual(count, 6)
        self.assertTrue(_check4)
        return

    def test_update_03(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_05()
        _new = get_data_07()
        sql_filter = "testid = ?"

        count = _sqlite.insert(_table.name, _table.names, _data)

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_integrity_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock
        _check3 = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertEqual(count, 6)
        self.assertTrue(_check4)
        return

    def test_update_04(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_05()
        _new = get_data_07()
        sql_filter = "testid = ?"

        count = _sqlite.insert(_table.name, _table.names, _data)

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_operational_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock
        _check3 = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertEqual(count, 6)
        self.assertTrue(_check4)
        return

    def test_update_05(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()

        _check2 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_05()
        _new = get_data_08()
        sql_filter = "testid = ?"

        count = _sqlite.insert(_table.name, _table.names, _data)

        _check3 = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)

        _check4 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertFalse(_check3)
        self.assertEqual(count, 6)
        self.assertTrue(_check4)
        return

    def test_select_01(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()
        _count1 = _sqlite.count_table(_table.name)

        _data_list = _sqlite.select(table_name=_table.name, names=[], sql_filter="", data=[])
        _count2 = len(_data_list)

        _check4 = _sqlite.disconnect()

        _data = (1, True, "Test01", "testers/")
        _check_data = _data_list[0]

        self.assertTrue(_check1)
        self.assertEqual(_count1, 6)
        self.assertEqual(_count2, 6)
        self.assertSequenceEqual(_data, _check_data)
        self.assertTrue(_check4)
        return

    def test_select_02(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()
        _count1 = _sqlite.count_table(_table.name)

        sql_filter = "testid = ?"
        data_filter = [1]

        _data_list = _sqlite.select(table_name=_table.name, names=[], sql_filter=sql_filter, data=data_filter)
        _count2 = len(_data_list)

        _check4 = _sqlite.disconnect()

        _data = (1, True, "Test01", "testers/")
        _check_data = _data_list[0]

        self.assertTrue(_check1)
        self.assertEqual(_count1, 6)
        self.assertEqual(_count2, 1)
        self.assertSequenceEqual(_data, _check_data)
        self.assertTrue(_check4)
        return

    def test_select_03(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()
        _count1 = _sqlite.count_table(_table.name)

        sql_filter = "testid = ?"
        data_filter = [1]
        names = [
            "testid",
            "use_test"
        ]

        _data_list = _sqlite.select(table_name=_table.name, names=names, sql_filter=sql_filter, data=data_filter)
        _count2 = len(_data_list)

        _check4 = _sqlite.disconnect()

        _data = (1, True)
        _check_data = _data_list[0]

        self.assertTrue(_check1)
        self.assertEqual(_count1, 6)
        self.assertEqual(_count2, 1)
        self.assertSequenceEqual(_data, _check_data)
        self.assertTrue(_check4)
        return

    def test_select_04(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()
        _count1 = _sqlite.count_table(_table.name)

        sql_filter = "testid = ?"
        data_filter = [1]
        names = [
            "testid",
            "use_test"
        ]

        _sqlite.connection = None

        _data_list = _sqlite.select(table_name=_table.name, names=names, sql_filter=sql_filter, data=data_filter)

        self.assertTrue(_check1)
        self.assertEqual(_count1, 6)
        self.assertIsNone(_data_list)
        return

    def test_select_05(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()
        _count1 = _sqlite.count_table(_table.name)

        sql_filter = "testid = ?"
        data_filter = [1]
        names = [
            "testid",
            "use_test"
        ]

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_operational_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _sqlite.connection = _class_mock

        _data_list = _sqlite.select(table_name=_table.name, names=names, sql_filter=sql_filter, data=data_filter)

        self.assertTrue(_check1)
        self.assertEqual(_count1, 6)
        self.assertIsNone(_data_list)
        return

    def test_select_06(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(_sqlite)

        _check1 = _sqlite.connect()
        _count1 = _sqlite.count_table(_table.name)

        sql_filter = "testid = ?"
        data_filter = [15235670141346654134]
        names = [
            "testid",
            "use_test"
        ]

        _data_list = _sqlite.select(table_name=_table.name, names=names, sql_filter=sql_filter, data=data_filter)

        self.assertTrue(_check1)
        self.assertEqual(_count1, 6)
        self.assertIsNone(_data_list)
        return
