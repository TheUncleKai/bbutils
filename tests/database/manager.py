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
from bbutil.database.sqlite.manager import Connection
from bbutil.utils import full_path

from tests.helper.sqlite import (sqlite_operational_error, sqlite_integrity_error, sqlite_unknown_error,
                                 mock_operational_error, get_table_01, get_data_01,
                                 get_data_02, get_data_03, get_data_04, get_data_05, get_data_06, get_data_07,
                                 get_data_08)

from tests.helper import get_sqlite, set_log

__all__ = [
    "TestSQLiteManager"
]


class TestSQLiteManager(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_setup_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        self.assertEqual(_connection.filename, _testfile)
        self.assertEqual(_connection.use_memory, False)
        self.assertIsNotNone(_connection._lock)
        return

    def test_setup_02(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(use_memory=True)

        self.assertEqual(_connection.filename, "")
        self.assertEqual(_connection.use_memory, True)
        self.assertIsNotNone(_connection._lock)
        return

    def test_connect_01(self):
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _connection = Connection()
        _connection.setup(filename=_testfile, use_memory=False)

        self.assertEqual(_connection.filename, _testfile)
        self.assertEqual(_connection.use_memory, False)
        self.assertIsNotNone(_connection._lock)

        _check = _connection.connect()
        c = _connection.cursor()
        self.assertTrue(_check)
        self.assertIsNotNone(_connection.connection)
        self.assertIsNotNone(c)

        _check = _connection.release()
        self.assertTrue(_check)
        return
