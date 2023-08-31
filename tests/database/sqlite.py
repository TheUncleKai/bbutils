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

from tests.helper.sqlite import sqlite_operational_error, sqlite_integrity_error, sqlite_unknown_error
from tests.helper.sqlite import get_sqlite_operational_error, get_sqlite_integrity_error, get_sqlite_return_false
from tests.helper.sqlite import (get_table_01, get_data_01, get_data_02, get_data_03, get_data_04, get_data_05,
                                 get_data_06, get_data_07, get_data_08)

from tests.helper import get_sqlite, set_log, copy_sqlite

__all__ = [
    "TestSQLite"
]


class TestSQLite(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    @staticmethod
    def _clean(sqlite: SQLite):
        if os.path.exists(sqlite.filename) is True:
            os.remove(sqlite.filename)
        return

    def test_prepare_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _sqlite = SQLite(filename=_testfile, name="Test")

        self.assertIsNone(_sqlite.manager)

        _sqlite.prepare()
        _sqlite.prepare()

        self.assertEqual(_sqlite.name, _name)
        self.assertEqual(_sqlite.filename, _testfile)
        self.assertIsNotNone(_sqlite.manager)

        self._clean(_sqlite)
        return

    def test_check_01(self):
        _sqlite = get_sqlite(filename="test.sqlite")
        _sqlite.prepare()

        _check = _sqlite.check("Test")
        self.assertFalse(_check)

        self._clean(_sqlite)
        return

    def test_check_02(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _check = _sqlite.check("tester01")
        self.assertTrue(_check)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_check_03(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _check = _sqlite.check("tester01")
        self.assertFalse(_check)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_check_04(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _check = _sqlite.check("tester01")
        self.assertFalse(_check)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.connect', new=get_sqlite_return_false())
    def test_check_05(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _check = _sqlite.check("tester01")
        self.assertFalse(_check)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.release', new=get_sqlite_return_false())
    def test_check_06(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _check = _sqlite.check("tester01")
        self.assertFalse(_check)
        return

    def test_count_01(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _count = _sqlite.count("tester01")
        self.assertEqual(_count, 0)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_count_02(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _count = _sqlite.count("tester01")
        self.assertEqual(_count, -1)
        return

    def test_count_03(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _count = _sqlite.count("tester01")
        self.assertEqual(_count, 6)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.connect', new=get_sqlite_return_false())
    def test_count_04(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _count = _sqlite.count("tester01")
        self.assertEqual(_count, -1)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.release', new=get_sqlite_return_false())
    def test_count_05(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _count = _sqlite.count("tester01")
        self.assertEqual(_count, -1)
        return

    def test_prepare_table_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)
        self.assertEqual(_count, 0)

        _check = _sqlite.check("tester01")
        self.assertTrue(_check)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)
        self.assertEqual(_count, 0)
        self._clean(_sqlite)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.connect', new=get_sqlite_return_false())
    def test_prepare_table_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)
        self.assertEqual(_count, -1)
        self._clean(_sqlite)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.release', new=get_sqlite_return_false())
    def test_prepare_table_03(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)
        self.assertEqual(_count, -1)
        self._clean(_sqlite)
        return

    def test_prepare_table_04(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        self.assertEqual(_count, 6)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.release', new=get_sqlite_return_false())
    def test_prepare_table_05(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        self.assertEqual(_count, -1)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_prepare_table_06(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list, True)
        self.assertEqual(_count, -1)
        self._clean(_sqlite)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.commit', new=get_sqlite_return_false())
    def test_prepare_table_07(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        _count = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)
        self.assertEqual(_count, -1)
        self._clean(_sqlite)
        return

    def test_insert_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        count1 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_01()
        count2 = _sqlite.insert(_table.name, _table.names, _data)
        count3 = _sqlite.count(_table.name)

        self.assertEqual(count1, 0)
        self.assertEqual(count2, 1)
        self.assertEqual(count3, 1)
        self._clean(_sqlite)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.connect', new=get_sqlite_return_false())
    def test_insert_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _data = get_data_01()
        count = _sqlite.insert(_table.name, _table.names, _data)
        self.assertEqual(count, -1)
        self._clean(_sqlite)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.release', new=get_sqlite_return_false())
    def test_insert_03(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_01()

        count = _sqlite.insert(_table.name, _table.names, _data)

        self.assertEqual(count, -1)

        os.remove(_sqlite.filename)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.commit', new=get_sqlite_return_false())
    def test_insert_04(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_01()

        count = _sqlite.insert(_table.name, _table.names, _data)

        self.assertEqual(count, -1)

        os.remove(_sqlite.filename)
        return

    def test_insert_05(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        count1 = _sqlite.prepare_table(_table.name, _table.column_list, _table.unique_list)

        _data = get_data_02()
        count2 = _sqlite.insert(_table.name, _table.names, _data)
        count3 = _sqlite.count(_table.name)

        self.assertEqual(count1, 0)
        self.assertEqual(count2, -1)
        self.assertEqual(count3, 0)
        self._clean(_sqlite)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_insert_06(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_01()

        count = _sqlite.insert(_table.name, _table.names, _data)
        self.assertEqual(count, -1)

        self._clean(_sqlite)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_integrity_error())
    def test_insert_07(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_01()

        count = _sqlite.insert(_table.name, _table.names, _data)
        self.assertEqual(count, -1)

        self._clean(_sqlite)
        return

    def test_insert_08(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_03()

        count = _sqlite.insert(_table.name, _table.names, _data)
        self.assertEqual(count, -1)

        self._clean(_sqlite)
        return

    def test_insert_09(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_04()

        count = _sqlite.insert(_table.name, _table.names, _data)
        self.assertEqual(count, -1)

        self._clean(_sqlite)
        return

    def test_insert_10(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_05()

        count = _sqlite.insert(_table.name, _table.names, _data)
        self.assertEqual(count, 6)

        self._clean(_sqlite)
        return

    def test_insert_11(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _data = get_data_06()

        count = _sqlite.insert(_table.name, _table.names, _data)
        self.assertEqual(count, -1)

        self._clean(_sqlite)
        return

    def test_update_01(self):
        _sqlite = copy_sqlite(filename="test_update.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _new = get_data_07()
        sql_filter = "testid = ?"

        _check = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)
        self.assertTrue(_check)

        self._clean(_sqlite)
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
