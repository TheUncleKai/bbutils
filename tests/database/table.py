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
from tests.database.helper.table import get_table_01

__all__ = [
    "TestTable"
]


class TestTable(unittest.TestCase):
    """Testing class for locking module."""

    def tearDown(self):
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
