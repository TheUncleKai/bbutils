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

from dataclasses import dataclass
from typing import Optional

from tests.database.helper import set_log
from bbutil.database import Types, Table, Database

__all__ = [
    "TestData"
]


@dataclass
class TestData(Database):

    table01: Optional[Table] = None
    table02: Optional[Table] = None

    def init(self):
        self.log = set_log()
        self.name = "Testos"
        return

    def prepare(self, **kwargs) -> bool:
        _table = Table(name="tester01", sqlite=self.sqlite, log=self.log)
        _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)
        self.table01 = _table

        _table = Table(name="tester02", sqlite=self.sqlite, log=self.log)
        _table.add_column(name="testid", data_type=Types.integer, primarykey=True)
        _table.add_column(name="use_test", data_type=Types.bool)
        _table.add_column(name="category", data_type=Types.string, keyword=True)
        _table.add_column(name="testname", data_type=Types.string)
        _table.add_column(name="path", data_type=Types.string)
        self.table02 = _table
        return True

    def clear(self):
        self.table01.clear()
        self.table02.clear()
        return
