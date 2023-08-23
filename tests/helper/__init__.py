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

import bbutil
from bbutil import Logging

from bbutil.database import SQLite
from bbutil.utils import full_path

__all__ = [
    "database",
    "execute",
    "file",
    "setup",
    "sqlite",
    "table",
    "worker",

    "get_sqlite",
    "set_log"
]

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}


def get_sqlite(filename: str, path: str = os.getcwd(), clean: bool = False) -> SQLite:
    _testfile = full_path("{0:s}/{1:s}".format(path, filename))
    _name = "Test"

    if (os.path.exists(_testfile) is True) and (clean is True):
        os.remove(_testfile)

    _sqlite = SQLite(filename=_testfile, name="Test")
    return _sqlite


def set_log():
    if bbutil.log is not None:
        return

    _log = Logging()
    _log.setup(app="Test", level=2, index=_index)

    console = _log.get_writer("console")
    _log.register(console)
    _log.open()

    bbutil.set_log(_log)
    return
