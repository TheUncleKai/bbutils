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

import bbutil

from bbutil.database import Table, Types, SQLite

from tests.helper import get_sqlite, set_log
from tests.helper.table import TestData, get_table_01, get_table_02, get_table_03, get_table_04

from tests.helper.sqlite import get_sqlite_operational_error, get_sqlite_integrity_error, get_sqlite_return_false

__all__ = [
    "TestTable"
]


class TestTable(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    @staticmethod
    def _clean(sqlite: SQLite):
        if os.path.exists(sqlite.filename) is True:
            os.remove(sqlite.filename)
        return

    def assertHasAttr(self, obj, intended_attr):
        _testBool = hasattr(obj, intended_attr)

        self.assertTrue(_testBool, msg=f'obj lacking an attribute. {obj=}, {intended_attr=}')
        return

    def test_add_column_01(self):

        _sqlite = get_sqlite(filename="test.sqlite", clean=True)

        _table = Table(name="test01", sqlite=_sqlite)
        _table.add_column(name="testid", data_type=Types.integer, unique=True, keyword=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)

        _names = [
            "testid",
            "use_test",
            "testname",
            "path"
        ]

        _column_list = [
            '"testid" INTEGER',
            '"use_test" BOOLEAN',
            '"testname" TEXT',
            '"path" TEXT'
        ]

        _unique_list = [
            "testid"
        ]

        _count1 = len(_table.names)
        _count2 = len(_table.columns)

        self.assertEqual(_table.keyword, "testid")
        self.assertEqual(_count1, 4)
        self.assertEqual(_count2, 4)
        self.assertListEqual(_names, _table.names)
        self.assertListEqual(_column_list, _table.column_list)
        self.assertListEqual(_unique_list, _table.unique_list)
        self._clean(_table.sqlite)
        return

    def test_add_column_02(self):

        _sqlite = get_sqlite(filename="test.sqlite", clean=True)

        _table = Table(name="test01", sqlite=_sqlite)
        _table.add_column(name="testid", data_type=Types.integer, unique=True, keyword=True)
        _table.add_column(name="testid", data_type=Types.integer)

        _count1 = len(_table.names)

        self.assertEqual(_count1, 1)
        self._clean(_table.sqlite)
        return

    def test_new_data_01(self):

        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(sqlite_object=_sqlite)

        _data = _table.new_data()
        self.assertHasAttr(_data, "testid")
        self.assertHasAttr(_data, "use_test")
        self.assertHasAttr(_data, "testname")
        self.assertHasAttr(_data, "path")
        self._clean(_table.sqlite)
        return

    def test_init_01(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)

        _check = _table.init()
        self.assertTrue(_check)
        return

    def test_init_02(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = Table(name="test01", sqlite=_sqlite)

        _check = _table.init()
        self.assertFalse(_check)
        return

    @mock.patch('sqlite3.connect', new=get_sqlite_operational_error())
    def test_init_03(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)

        _check = _table.init()
        self.assertFalse(_check)
        return

    def test_init_04(self):
        bbutil.set_log(None)

        _table = Table(name="Testos")
        _check1 = _table.init()
        self.assertFalse(_check1)
        return

    def test_select_01(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data = _table.select()
        _count = len(_data)

        self.assertTrue(_check2)
        self.assertEqual(_count, 6)
        return

    def test_select_02(self):
        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)
        _table.suppress_warnings = False

        _check2 = _table.init()

        _data = _table.select()
        _count = len(_data)

        self.assertTrue(_check2)
        self.assertEqual(_count, 0)
        return

    def test_select_03(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)
        _table.suppress_warnings = False

        _check2 = _table.init()

        with mock.patch('sqlite3.connect', new=get_sqlite_operational_error()):
            _data = _table.select()

        _count = len(_data)

        self.assertTrue(_check2)
        self.assertEqual(_count, 0)
        return

    def test_select_04(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_02(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data = _table.select()
        _count = len(_data)

        self.assertTrue(_check2)
        self.assertEqual(_count, 0)
        return

    def test_store_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data = _table.new_data()
        _data.use_test = True
        _data.testname = "Test01"
        _data.path = "path"

        _count = _table.store(_data)

        self.assertTrue(_check2)
        self.assertEqual(_count, 1)
        self._clean(_table.sqlite)
        return

    def test_store_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data1 = _table.new_data()
        _data1.testid = 0
        _data1.use_test = True
        _data1.testname = "Test01"
        _data1.path = "path"

        _data2 = _table.new_data()
        _data2.testid = 1
        _data2.use_test = True
        _data2.testname = "Test02"
        _data2.path = "path"

        _table.add(_data1)
        _table.add(_data2)

        _count = _table.store()

        self.assertTrue(_check2)
        self.assertEqual(_count, 2)
        self._clean(_table.sqlite)
        return

    def test_store_03(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data1 = _table.new_data()
        _data1.testid = 0
        _data1.use_test = True
        _data1.testname = "Test01"
        _data1.path = "path"

        _data2 = _table.new_data()
        _data2.testid = 1
        _data2.use_test = True
        _data2.testname = "Test02"
        _data2.path = "path"

        _data3 = _table.new_data()
        _data3.testid = 1
        _data3.use_test = True
        _data3.testname = "Test02"
        _data3.path = "path"

        _table.add(_data1)
        _table.add(_data2)
        _table.add(_data3)

        _count = _table.store()

        self.assertTrue(_check2)
        self.assertEqual(_count, 2)
        self._clean(_table.sqlite)
        return

    def test_add_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_04(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data1 = _table.new_data()
        _data1.use_test = True
        _data1.category = "TestMain"
        _data1.testname = "Test01"
        _data1.path = "path"

        _data2 = _table.new_data()
        _data2.use_test = True
        _data2.category = "TestMain"
        _data2.testname = "Test02"
        _data2.path = "path"

        _data3 = _table.new_data()
        _data3.use_test = True
        _data3.category = "TestOther"
        _data3.testname = "Test02"
        _data3.path = "path"

        _table.add(_data1)
        _table.add(_data2)
        _table.add(_data3)

        _list1 = _table.index["TestMain"]
        _list2 = _table.index["TestOther"]

        self.assertTrue(_check2)
        self.assertEqual(len(_list1), 2)
        self.assertEqual(len(_list2), 1)
        self._clean(_table.sqlite)
        return

    def test_add_02(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_04(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data1 = _table.new_data()
        _data1.use_test = True
        _data1.category = "TestMain"
        _data1.testname = "Test01"
        _data1.path = "path"

        _data2 = TestData()
        _data2.use_test = True
        _data2.xcategory = "TestMain"
        _data2.testname = "Test01"
        _data2.path = "path"

        _table.add(_data1)

        # noinspection PyTypeChecker
        self.assertRaises(Exception, _table.add, _data2)

        _list1 = _table.index["TestMain"]

        self.assertTrue(_check2)
        self.assertEqual(len(_list1), 1)
        self._clean(_table.sqlite)
        return

    def test_update_01(self):
        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_04(sqlite_object=_sqlite)

        _check2 = _table.init()

        _data1 = _table.new_data()
        _data1.use_test = True
        _data1.category = "TestMain"
        _data1.testname = "Test01"
        _data1.path = "path"

        _table.add(_data1)
        _check3 = _table.store()

        _data2 = _table.new_data()
        _data2.use_test = True
        _data2.category = "TestMain"
        _data2.testname = "Test02"
        _data2.path = "path"

        _check4 = _table.update(_data2, "testid = ?", 1)
        _count = _table.check()

        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertTrue(_check4)
        self.assertEqual(_count, 1)
        self._clean(_table.sqlite)
        return

    def _load_table(self, table: Table, limit: int):
        _sql_count = table.check()
        _data_count = table.load()

        self.assertEqual(_sql_count, limit)
        self.assertEqual(_data_count, limit)
        return

    def test_load_01(self):
        _sqlite = get_sqlite(filename="test_bulk.sqlite", path="testdata/database")

        _table0 = get_table_03("interval0", sqlite_object=_sqlite)
        _table1 = get_table_03("interval1", sqlite_object=_sqlite)
        _table2 = get_table_03("interval2", sqlite_object=_sqlite)
        _table3 = get_table_03("interval3", sqlite_object=_sqlite)
        _table4 = get_table_03("interval4", sqlite_object=_sqlite)
        _table5 = get_table_03("interval5", sqlite_object=_sqlite)
        _table6 = get_table_03("interval6", sqlite_object=_sqlite)

        _tables = [
            _table0,
            _table1,
            _table2,
            _table3,
            _table4,
            _table5,
            _table6
        ]

        for _table in _tables:
            _check = _table.init()
            self.assertTrue(_check)

        self._load_table(_table0, 500)
        self._load_table(_table1, 1000)
        self._load_table(_table2, 5000)
        self._load_table(_table3, 10000)
        self._load_table(_table4, 20000)
        self._load_table(_table5, 50000)
        self._load_table(_table6, 100000)
        return

    def test_load_02(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")

        _table = get_table_01(sqlite_object=_sqlite)

        _check_init = _table.init()

        with mock.patch('sqlite3.connect', new=get_sqlite_operational_error()):
            _count = _table.load()

        self.assertTrue(_check_init)
        self.assertEqual(_count, 0)
        return

    def test_clear_01(self):
        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")

        _table = get_table_01(sqlite_object=_sqlite)

        _check_init = _table.init()
        _count1 = _table.load()

        _table.clear()

        _count2 = _table.data_count

        self.assertTrue(_check_init)
        self.assertEqual(_count1, 6)
        self.assertEqual(_count2, 0)
        return
