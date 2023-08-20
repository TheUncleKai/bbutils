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

import sqlite3
from unittest import mock as mock

from bbutil.logging import Logging
from bbutil.utils import full_path
from bbutil.database import SQLite, Types, Table, Data

__all__ = [
    "sqlite_crash_error",
    "mock_crash_error",

    "set_log",
    "get_sqlite",
    "get_table_01",
    "get_data_01",
    "get_data_02"
]

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}

sqlite_crash_error = sqlite3.OperationalError('This did go boing!!')
mock_crash_error = mock.Mock(side_effect=sqlite_crash_error)


def set_log() -> Logging:
    _log = Logging()
    _log.setup(app="Test", level=2, index=_index)

    console = _log.get_writer("console")
    _log.register(console)
    _log.open()
    return _log


def get_sqlite(filename: str, path: str = os.getcwd(), clean: bool = False) -> SQLite:
    _log = set_log()
    _testfile = full_path("{0:s}/{1:s}".format(path, filename))
    _name = "Test"

    if (os.path.exists(_testfile) is True) and (clean is True):
        os.remove(_testfile)

    _sqlite = SQLite(filename=_testfile, name="Test", log=_log)
    return _sqlite


def get_table_01(sqlite_object: SQLite) -> Table:
    _table = Table(name="tester01", sqlite=sqlite_object)
    _table.add_column(name="testid", data_type=Types.integer, unique=True)
    _table.add_column(name="use_test", data_type=Types.bool)
    _table.add_column(name="testname", data_type=Types.string)
    _table.add_column(name="path", data_type=Types.string)
    return _table


def get_data_01() -> Data:
    _names = [
        "testid",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        1,
        True,
        "Test01",
        "testers/"
    ]

    _data = Data(_names, _values)
    return _data


def get_data_02() -> Data:
    _names = [
        "testidx",
        "use_test",
        "testname",
        "path"
    ]

    _values = [
        1,
        True,
        "Test01",
        "testers/"
    ]

    _data = Data(_names, _values)
    return _data


class Data01(object):

    def __init__(self):
        self.testid: int = 0
        self.use_test: bool = False
        self.testname: str = ""
        self.path: str = ""
        return
