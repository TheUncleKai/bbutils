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

from bbutil.database import SQLite
from bbutil.utils import full_path

__all__ = [
    "sqlite",
    "table",

    "get_sqlite"
]


def get_sqlite(filename: str, path: str = os.getcwd(), clean: bool = False) -> SQLite:
    _testfile = full_path("{0:s}/{1:s}".format(path, filename))
    _name = "Test"

    if (os.path.exists(_testfile) is True) and (clean is True):
        os.remove(_testfile)

    _sqlite = SQLite(filename=_testfile, name="Test")
    return _sqlite
