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

from tests.database.helper import set_log
from tests.database.helper.database import TestData

from tests.database.helper.sqlite import (mock_operational_error, sqlite_operational_error)

__all__ = [
    "TestDatabase"
]


class TestDatabase(unittest.TestCase):
    """Testing class for locking module."""

    def tearDown(self):
        return

    def assertHasAttr(self, obj, intended_attr):
        _testBool = hasattr(obj, intended_attr)

        self.assertTrue(_testBool, msg=f'obj lacking an attribute. {obj=}, {intended_attr=}')
        return

    def test_start_01(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())

        _database = TestData(filename=_filename)

        _check1 = _database.start()
        self.assertIsNotNone(_database.table01)
        self.assertIsNotNone(_database.table02)

        _check2 = _database.stop()

        self.assertTrue(_check1)
        self.assertTrue(_check2)
        return

    def test_start_02(self):
        _database = TestData(filename="")

        _check1 = _database.start()

        self.assertFalse(_check1)
        return

    def test_start_03(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename, prepare_fail=True)

        _check1 = _database.start()

        self.assertFalse(_check1)
        return

    @mock.patch('sqlite3.connect', new=mock_operational_error)
    def test_start_04(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())
        _database = TestData(filename=_filename)

        _check1 = _database.start()

        self.assertFalse(_check1)
        return

    def test_start_05(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())

        _cursor_mock = Mock()
        _cursor_mock.execute = Mock(side_effect=sqlite_operational_error)

        _class_mock = Mock()
        _class_mock.cursor = Mock(return_value=_cursor_mock)

        _database = TestData(filename=_filename, mock_connection=_class_mock)

        _check1 = _database.start()

        self.assertFalse(_check1)
        return

    def test_stop_01(self):
        _filename = "{0:s}/test.sqlite".format(os.getcwd())

        _database = TestData(filename=_filename, log=set_log())

        _check1 = _database.stop()

        self.assertFalse(_check1)
        return
