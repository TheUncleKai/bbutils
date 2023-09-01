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

from bbutil.database import SQLite, Table
from bbutil.utils import full_path

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

    def test_prepare_table_08(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _sqlite.prepare()
        _table = get_table_01(_sqlite)

        with mock.patch('sqlite3.connect', new=get_sqlite_operational_error()):
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

        _sqlite.manager.reset()

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

    @staticmethod
    def _fill_bulk(table: Table, max_range: int = 0):
        _range = range(0, max_range)
        _width = len(str(max_range))

        for _number in _range:
            _data = table.new_data()
            _data.testid = _number
            _data.use_test = True
            _testname = "Test{0:s}".format(str(_number).rjust(_width, "0"))
            _data.testname = _testname
            _data.path = "/blo/bka/{0:s}".format(_testname)
            table.add(_data)
        return

    def test_bulk_insert_01(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 500)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 500)

        self._clean(_sqlite)
        return

    def test_bulk_insert_02(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 1000)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 1000)

        self._clean(_sqlite)
        return

    def test_bulk_insert_03(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 5000)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 5000)

        self._clean(_sqlite)
        return

    def test_bulk_insert_04(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 10000)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 10000)

        self._clean(_sqlite)
        return

    def test_bulk_insert_05(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 20000)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 20000)

        self._clean(_sqlite)
        return

    def test_bulk_insert_06(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 50000)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 50000)

        self._clean(_sqlite)
        return

    def test_bulk_insert_07(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 100000)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 100000)

        self._clean(_sqlite)
        return

    def test_bulk_insert_08(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 10)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 10)

        self._fill_bulk(_table, 10)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 0)

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

    @mock.patch('bbutil.database.sqlite.manager.Connection.connect', new=get_sqlite_return_false())
    def test_update_02(self):
        _sqlite = copy_sqlite(filename="test_update.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _new = get_data_07()
        sql_filter = "testid = ?"

        _check = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)
        self.assertFalse(_check)

        self._clean(_sqlite)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.release', new=get_sqlite_return_false())
    def test_update_03(self):
        _sqlite = copy_sqlite(filename="test_update.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _new = get_data_07()
        sql_filter = "testid = ?"

        _check = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)
        self.assertFalse(_check)

        self._clean(_sqlite)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.commit', new=get_sqlite_return_false())
    def test_update_04(self):
        _sqlite = copy_sqlite(filename="test_update.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _new = get_data_07()
        sql_filter = "testid = ?"

        _check = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)
        self.assertFalse(_check)

        self._clean(_sqlite)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_update_05(self):
        _sqlite = copy_sqlite(filename="test_update.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _new = get_data_07()
        sql_filter = "testid = ?"

        _check = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)
        self.assertFalse(_check)

        self._clean(_sqlite)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_integrity_error())
    def test_update_06(self):
        _sqlite = copy_sqlite(filename="test_update.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _new = get_data_07()
        sql_filter = "testid = ?"

        _check = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)
        self.assertFalse(_check)

        self._clean(_sqlite)
        return

    def test_update_07(self):
        _sqlite = copy_sqlite(filename="test_update.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _new = get_data_08()
        sql_filter = "testid = ?"

        _check = _sqlite.update(_table.name, _table.names, _new, sql_filter, 4)
        self.assertFalse(_check)

        self._clean(_sqlite)
        return

    def test_select_01(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _data_list = _sqlite.select(table_name=_table.name, names=[], sql_filter="", data=[])
        _count = len(_data_list)

        _data = (1, True, "Test01", "testers/")
        _check_data = _data_list[0]

        self.assertEqual(_count, 6)
        self.assertSequenceEqual(_data, _check_data)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.connect', new=get_sqlite_return_false())
    def test_select_02(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _data_list = _sqlite.select(table_name=_table.name, names=[], sql_filter="", data=[])
        self.assertIsNone(_data_list)
        return

    @mock.patch('bbutil.database.sqlite.manager.Connection.release', new=get_sqlite_return_false())
    def test_select_03(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        _data_list = _sqlite.select(table_name=_table.name, names=[], sql_filter="", data=[])
        self.assertIsNone(_data_list)
        return

    def test_select_04(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        sql_filter = "testid = ?"
        data_filter = [1]

        _data_list = _sqlite.select(table_name=_table.name, names=[], sql_filter=sql_filter, data=data_filter)
        _count2 = len(_data_list)

        _data = (1, True, "Test01", "testers/")
        _check_data = _data_list[0]

        self.assertEqual(_count2, 1)
        self.assertSequenceEqual(_data, _check_data)
        return

    def test_select_05(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        sql_filter = "testid = ?"
        data_filter = [1]
        names = [
            "testid",
            "use_test"
        ]

        _data_list = _sqlite.select(table_name=_table.name, names=names, sql_filter=sql_filter, data=data_filter)
        _count2 = len(_data_list)

        _data = (1, True)
        _check_data = _data_list[0]

        self.assertEqual(_count2, 1)
        self.assertSequenceEqual(_data, _check_data)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_select_06(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        sql_filter = "testid = ?"
        data_filter = [1]
        names = [
            "testid",
            "use_test"
        ]

        _data_list = _sqlite.select(table_name=_table.name, names=names, sql_filter=sql_filter, data=data_filter)
        self.assertIsNone(_data_list)
        return

    def test_select_07(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)

        sql_filter = "testid = ?"
        data_filter = [15235670141346654134]
        names = [
            "testid",
            "use_test"
        ]

        _data_list = _sqlite.select(table_name=_table.name, names=names, sql_filter=sql_filter, data=data_filter)

        self.assertIsNone(_data_list)
        return

    def _compare_bulk(self, data):
        _width = len(str(500))

        _number = 0
        for item in data:
            item_testid = item[0]
            item_use_test = item[1]
            item_testname = item[2]
            item_path = item[3]

            self.assertEqual(item_testid, _number)
            self.assertTrue(item_use_test)

            _testname = "Test{0:s}".format(str(_number).rjust(_width, "0"))
            _path = "/blo/bka/{0:s}".format(_testname)
            self.assertEqual(item_testname, _testname)
            self.assertEqual(item_path, _path)

            _number += 1
        return

    def test_bulk_insert_select_01(self):
        _sqlite = copy_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _sqlite.prepare()

        _table = get_table_01(_sqlite)
        _table.name = "tester01"

        self._fill_bulk(_table, 500)

        count = _sqlite.insert(_table.name, _table.names, _table.data)
        self.assertEqual(count, 500)

        data = _sqlite.select(_table.name, _table.names, "", [])
        count = len(data)
        self.assertEqual(count, 500)

        self._compare_bulk(data)

        self._clean(_sqlite)
        return
