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

import abc
from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Optional, List

from bbutil.logging import Logging

from bbutil.database.sqlite import SQLite
from bbutil.database.types import Data
from bbutil.database.table import Table

__all__ = [
    "Database"
]


@dataclass
class Database(metaclass=ABCMeta):

    log: Optional[Logging] = None

    name: str = ""
    sqlite: Optional[SQLite] = None
    tables: List[Table] = field(default_factory=list)
    filename: str = ""

    def add(self, table: str, data: Data):
        for _table in self.tables:
            if _table.name == table:
                _table.add(data)
                return
        return

    def get_table(self, table_id: str) -> Optional[Table]:
        for _table in self.tables:
            if _table.name == table_id:
                return _table

        return None

    def info(self):
        for _table in self.tables:
            _count = len(_table.data)
            _line = "{0:s}: {1:d}".format(_table.name, _count)
            self.log.inform(self.name, _line)
        return

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def prepare(self, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    def clear_data(self):
        pass

    def clear(self):
        for _table in self.tables:
            _table.clear()

        self.clear_data()
        return

    def store(self):
        for _table in self.tables:
            _table.store()
        return

    def start(self) -> bool:
        self.init()

        if (self.name == "") or (self.filename == ""):
            self.log.error("File- or database-name is missing!")
            return False

        self.sqlite = SQLite(name=self.name, filename=self.filename, log=self.log)

        _check = self.prepare()
        if _check is False:
            return False

        _check = self._open()
        if _check is False:
            return False
        return True

    def _open(self) -> bool:
        if self.sqlite is None:
            self.log.error("No SQLite connection established!")
            return False

        _check = self.sqlite.connect()
        if _check is False:
            return False

        for _table in self.tables:
            _check = _table.init()
            if _check is False:
                return False

        return True

    def stop(self) -> bool:
        if self.sqlite is None:
            self.log.error("No SQLite connection established!")
            return False

        self.log.inform(self.name, "Close connection!")
        _check = self.sqlite.disconnect()
        if _check is False:
            return False

        del self.sqlite
        self.sqlite = None

        self.clear()
        return True
