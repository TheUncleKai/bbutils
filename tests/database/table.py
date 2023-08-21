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

from bbutil.database import SQLite, Table, Types
from bbutil.utils import full_path

from tests.database.helper import get_sqlite
from tests.database.helper.table import get_table_01, get_table_02

__all__ = [
    "TestTable"
]


class TestTable(unittest.TestCase):
    """Testing class for locking module."""

    def tearDown(self):
        return

    def assertHasAttr(self, obj, intended_attr):
        _testBool = hasattr(obj, intended_attr)

        self.assertTrue(_testBool, msg=f'obj lacking an attribute. {obj=}, {intended_attr=}')
        return

    def test_add_column_01(self):

        _sqlite = get_sqlite(filename="test.sqlite", clean=True)

        _table = Table(name="test01", sqlite=_sqlite, log=_sqlite.log)
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
        return

    def test_add_column_02(self):

        _sqlite = get_sqlite(filename="test.sqlite", clean=True)

        _table = Table(name="test01", sqlite=_sqlite, log=_sqlite.log)
        _table.add_column(name="testid", data_type=Types.integer, unique=True, keyword=True)
        _table.add_column(name="testid", data_type=Types.integer)

        _count1 = len(_table.names)

        self.assertEqual(_count1, 1)
        return

    def test_new_data_01(self):

        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(sqlite_object=_sqlite)

        _data = _table.new_data()
        self.assertHasAttr(_data, "testid")
        self.assertHasAttr(_data, "use_test")
        self.assertHasAttr(_data, "testname")
        self.assertHasAttr(_data, "path")
        return

    def test_init_01(self):

        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)

        _check1 = _sqlite.connect()
        _check2 = _table.init()
        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_init_02(self):

        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = Table(name="test01", sqlite=_sqlite, log=_sqlite.log)

        _check1 = _sqlite.connect()
        _check2 = _table.init()
        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        self.assertTrue(_check3)
        return

    def test_init_03(self):

        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)

        _check1 = _sqlite.connect()
        _sqlite.connection = None
        _check2 = _table.init()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        return

    def test_select_01(self):

        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)

        _check1 = _sqlite.connect()
        _check2 = _table.init()

        _data = _table.select()
        _count = len(_data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertEqual(_count, 6)
        return

    def test_select_02(self):

        _sqlite = get_sqlite(filename="test_check_table.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)
        _table.suppress_warnings = False

        _check1 = _sqlite.connect()
        _check2 = _table.init()

        _data = _table.select()
        _count = len(_data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertEqual(_count, 0)
        return

    def test_select_03(self):

        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_01(sqlite_object=_sqlite)
        _table.suppress_warnings = False

        _check1 = _sqlite.connect()
        _check2 = _table.init()

        _sqlite.connection = None
        _data = _table.select()
        _count = len(_data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertEqual(_count, 0)
        return

    def test_select_04(self):

        _sqlite = get_sqlite(filename="test_select.sqlite", path="testdata/database")
        _table = get_table_02(sqlite_object=_sqlite)

        _check1 = _sqlite.connect()
        _check2 = _table.init()

        _data = _table.select()
        _count = len(_data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertEqual(_count, 0)
        return

    def test_store_01(self):

        _sqlite = get_sqlite(filename="test.sqlite", clean=True)
        _table = get_table_01(sqlite_object=_sqlite)

        _check1 = _sqlite.connect()
        _check2 = _table.init()

        _data = _table.new_data()
        _data.use_test = True
        _data.testname = "Test01"
        _data.path = "path"

        _count = _table.store(_data)

        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        self.assertEqual(_count, 1)
        return
