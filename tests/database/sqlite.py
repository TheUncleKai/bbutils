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
import sys
import sqlite3

from sqlite3 import Connection

from typing import Optional

import bbutil.lang.parser
import bbutil.lang.parser.pyfile

from unittest.mock import MagicMock, Mock
from bbutil.database.sqlite import SQLite
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

    def _get_sqlite(self) -> SQLite:
        _log = self.set_log()
        _testfile = full_path("{0:s}/test.sqlite".format(os.getcwd()))
        _name = "Test"

        if os.path.exists(_testfile) is True:
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

    def test_disconnect_01(self):
        _sqlite = self._get_sqlite()

        _check1 = _sqlite.connect()
        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        return

    def test_disconnect_02(self):
        _sqlite = self._get_sqlite()

        _check1 = _sqlite.connect()
        _check2 = _sqlite.disconnect()
        _check3 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        self.assertTrue(_check3)
        return

    def test_disconnect_03(self):
        _sqlite = self._get_sqlite()

        _check1 = _sqlite.connect()

        _sqlite.commit = True

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        return

    def test_disconnect_04(self):
        _sqlite = self._get_sqlite()

        _check1 = _sqlite.connect()

        _class_mock = Mock()
        _class_mock.commit = Mock(side_effect=crash_error)

        _sqlite.commit = True
        _sqlite.connection = _class_mock

        _check2 = _sqlite.disconnect()

        self.assertTrue(_check1)
        self.assertFalse(_check2)
        return
