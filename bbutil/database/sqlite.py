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

import sqlite3
from dataclasses import dataclass, field
from multiprocessing import Lock
from typing import Optional, List, Union

from bbutil.logging import Logging
from bbutil.database.types import Data

__all__ = [
    "Select",
    "SQLite"
]


@dataclass
class _Execute(object):

    data: list = field(default_factory=list)
    sql: str = ""


@dataclass
class Select(object):

    number: int = -1
    data: list = field(default_factory=list)


@dataclass
class SQLite(object):

    log: Optional[Logging] = None

    name: str = ""
    connection: Optional[sqlite3.Connection] = None
    commit: bool = False
    cursor: Optional[sqlite3.Cursor] = None
    use_memory: bool = False
    use_scrict: bool = False
    filename: str = ""
    lock: Optional[Lock] = None

    def _check_log(self):
        if self.log is None:
            raise ValueError("Logging class is missing!")
        return

    def connect(self) -> bool:
        self._check_log()

        if self.name == "":
            self.log.error("Connection is unnamed!")
            return False

        if (self.filename == "") and (self.use_memory is False):
            self.log.error("No filename given!")
            return False

        if self.lock is None:
            self.lock = Lock()

        self.log.debug1(self.name, "Acquire Lock")
        self.lock.acquire()

        if self.use_memory is True:
            try:
                self.connection = sqlite3.connect(':memory:',
                                                  detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            except sqlite3.OperationalError as e:
                self.log.error("Unable to create database in memory!")
                self.log.exception(e)
                return False

            self.filename = "memory"

            return True

        self.log.inform(self.name, "Connect to {0:s}".format(self.filename))

        try:
            self.connection = sqlite3.connect(self.filename,
                                              detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except sqlite3.OperationalError as e:
            self.log.error("Unable to create database: {0:s}".format(self.filename))
            self.log.exception(e)
            return False

        return True

    def disconnect(self) -> bool:
        self._check_log()

        if self.connection is None:
            return True

        if self.commit is True:
            try:
                self.connection.commit()
            except sqlite3.OperationalError as e:
                self.log.error("Unable to commit to database!")
                self.log.exception(e)
                return False

            self.commit = False

        self.log.debug1(self.name, "Close {0:s}".format(self.filename))

        try:
            self.connection.close()
        except sqlite3.OperationalError as e:
            self.log.error("Unable to close connection!")
            self.log.exception(e)
            return False

        self.connection = None
        self.lock.release()
        return True

    @property
    def is_connected(self) -> bool:
        if self.connection is None:
            return False
        return True

    def check_table(self, table_name: str) -> bool:
        self._check_log()

        if self.connection is None:
            self.log.error("No valid connection!")
            return False

        c = self.connection.cursor()
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0:s}';".format(table_name)

        self.log.debug1(self.name, "Check for table: {0:s}".format(table_name))

        try:
            c.execute(command)
        except sqlite3.OperationalError as e:
            self.log.error("Unable to check for table: {0:s}".format(table_name))
            self.log.exception(e)
            return False

        result = c.fetchone()
        if result is None:
            return False
        return True

    def count_table(self, table_name: str) -> int:
        self._check_log()

        if self.connection is None:
            self.log.error("No valid connection!")
            return -1

        c = self.connection.cursor()
        command = "SELECT count(*) FROM {0:s};".format(table_name)

        try:
            c.execute(command)
        except sqlite3.OperationalError as e:
            self.log.error("Unable to count rows: {0:s}".format(table_name))
            self.log.exception(e)
            return -1

        result = c.fetchall()
        (count,) = result[0]

        self.log.debug1(self.name, "Count table: {0:s}, {1:d}".format(table_name, count))
        return count

    def prepare_table(self, table_name: str, column_list: list, unique_list: list) -> bool:
        self._check_log()

        if self.connection is None:
            self.log.error("No valid connection!")
            return False

        _check = self.check_table(table_name)
        if _check is True:
            return True

        c = self.connection.cursor()

        _columns = ""

        for _line in column_list:
            if _columns == "":
                _columns = _line
            else:
                _columns = "{0:s}, {1:s}".format(_columns, _line)

        _constraint = ""
        if len(unique_list) > 0:
            _uniques = ", ".join(unique_list)
            _constraint = ", CONSTRAINT constraint_{0:s} UNIQUE ({1:s})".format(table_name, _uniques)

        command = 'CREATE TABLE "{0:s}" ({1:s}{2:s})'.format(table_name, _columns, _constraint)

        # if self.use_scrict is True:
        #     command = 'CREATE TABLE "{0:s}" ({1:s}{2:s}) STRICT'.format(table_name, _columns, _constraint)

        try:
            c.execute(command)
        except sqlite3.OperationalError as e:
            self.log.error("Unable to create table: {0:s}".format(table_name))
            self.log.exception(e)
            print(command)
            return False

        self.log.debug1(self.name, "Create table: {0:s}".format(table_name))

        self.connection.commit()
        return True

    def _single_execute(self, table_name: str, names: list, data: Data) -> Optional[_Execute]:
        _data = []
        _names = ", ".join(names)
        _placeholder = ", ".join(['?'] * len(names))

        sql = 'INSERT INTO "{0:s}" ({1:s}) VALUES ({2:s});'.format(table_name, _names, _placeholder)

        for _line in names:
            try:
                _value = getattr(data, _line)
            except AttributeError as e:
                self.log.exception(e)
                self.log.error("Data format does not fit database table!")
                return None
            _data.append(_value)
        _execute = _Execute(sql=sql, data=_data)
        return _execute

    def _many_execute(self, table_name: str, names: list, data_list: List[Data]) -> Optional[_Execute]:
        _data = []
        _length = len(data_list)
        _names = ", ".join(names)
        _placeholder = ", ".join(['?'] * len(names))

        sql = 'INSERT OR IGNORE INTO "{0:s}" ({1:s}) VALUES ({2:s});'.format(table_name, _names, _placeholder)

        for _item in data_list:
            _value = []
            for _line in names:
                try:
                    _ret = getattr(_item, _line)
                except AttributeError as e:
                    self.log.exception(e)
                    self.log.error("Data format does not fit database table!")
                    return None
                _value.append(_ret)
            _data.append(_value)

        _execute = _Execute(sql=sql, data=_data)
        return _execute

    def insert(self, table_name: str, names: list, data: Union[Data, List[Data]]) -> int:
        self._check_log()

        if self.connection is None:
            self.log.error("No valid connection!")
            return -1

        c = self.connection.cursor()

        _is_many = True

        if type(data) is Data:
            _is_many = False

        if _is_many is False:
            _execute = self._single_execute(table_name, names, data)
        else:
            _execute = self._many_execute(table_name, names, data)

        if _execute is None:
            return -1

        if _is_many is True:
            command = c.executemany
        else:
            command = c.execute

        try:
            command(_execute.sql, _execute.data)
        except sqlite3.InterfaceError as e:
            self.log.exception(e)
            self.log.error("One or more values is an invalid format!")
            self.log.error("SQL:  " + str(_execute.sql))
            self.log.error("DATA: " + str(_execute.data))
            return -1
        except OverflowError as e:
            self.log.exception(e)
            self.log.error("One or more values is too large!")
            self.log.error("SQL:  " + str(_execute.sql))
            self.log.error("DATA: " + str(_execute.data))
            return -1
        except sqlite3.IntegrityError:
            return -1
        except Exception as e:
            self.log.exception(e)
            self.log.error("SQL:  " + str(_execute.sql))
            self.log.error("DATA: " + str(_execute.data))
            return -1

        _counter = c.rowcount

        if _counter > 0:
            self.commit = True
        return _counter

    def update(self, table_name: str, names: list, data: Data, sql_filter: str, filter_value=None) -> bool:
        self._check_log()

        if self.connection is None:
            self.log.error("No valid connection!")
            return False

        c = self.connection.cursor()

        _sets = []
        for _name in names:
            _line = "{0:s} = ?".format(_name)
            _sets.append(_line)

        _data = []
        _names = ", ".join(_sets)

        sql = 'UPDATE "{0:s}" SET {1:s} WHERE {2:s};'.format(table_name, _names, sql_filter)

        for _line in names:
            _value = getattr(data, _line)
            _data.append(_value)

        if filter_value is not None:
            _data.append(filter_value)

        try:
            c.execute(sql, _data)
        except sqlite3.IntegrityError:
            return False
        except sqlite3.OperationalError as e:
            self.log.error("SQL:  " + str(sql))
            self.log.error("DATA: " + str(_data))
            self.log.exception(e)
            return False
        except Exception as e:
            self.log.exception(e)
            self.log.error("SQL:  " + str(sql))
            self.log.error("DATA: " + str(_data))
            return False
        except OverflowError as e:
            self.log.exception(e)
            self.log.error("SQL:  " + str(sql))
            self.log.error("DATA: " + str(_data))
            raise

        self.commit = True
        return True

    def select(self, table_name: str, sql_filter: str, names: list, data: list) -> Optional[list]:
        self._check_log()

        c = self.connection.cursor()

        _selector = "*"
        if len(names) != 0:
            _selector = ", ".join(names)

        command = "SELECT {0:s} FROM {1:s};".format(_selector, table_name)

        if sql_filter != "":
            command = "SELECT {0:s} FROM {1:s} WHERE {2:s};".format(_selector, table_name, sql_filter)

        self.log.debug1(table_name, command)

        if len(data) == 0:
            try:
                c.execute(command)
            except sqlite3.OperationalError as e:
                self.log.error("Unable to search table: {0:s}".format(table_name))
                self.log.error(command)
                self.log.exception(e)
                return None
        else:
            try:
                c.execute(command, data)
            except sqlite3.OperationalError as e:
                self.log.error("Unable to search table: {0:s}".format(table_name))
                print(command)
                print(data)
                self.log.exception(e)
                return None
            except OverflowError as e:
                self.log.error("Unable to search table: {0:s}".format(table_name))
                print(command)
                print(data)
                self.log.exception(e)
                raise

        _fetchlist = []

        for _data in c:
            _fetchlist.append(_data)

        return _fetchlist
