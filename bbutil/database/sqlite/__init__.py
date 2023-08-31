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
from dataclasses import dataclass
from typing import Optional, List, Union

import bbutil
from bbutil.database.sqlite.types import Execute
from bbutil.database.sqlite.manager import Connection
from bbutil.database.types import Data

__all__ = [
    "types",
    "manager",

    "SQLite"
]


@dataclass
class SQLite(object):

    name: str = ""
    manager: Optional[Connection] = None
    use_memory: bool = False
    use_scrict: bool = False
    filename: str = ""

    def prepare(self):
        if self.manager is not None:
            return

        self.manager: Connection = Connection()
        self.manager.setup(use_memory=self.use_memory, filename=self.filename)
        return

    def check(self, table_name: str) -> int:
        _check = self.manager.connect()
        if _check is False:
            return False

        _connection = self.manager.connection
        c = _connection.cursor()
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0:s}';".format(table_name)

        bbutil.log.debug1(self.name, "Check for table: {0:s}".format(table_name))

        try:
            c.execute(command)
        except sqlite3.OperationalError as e:
            bbutil.log.error("Unable to check for table: {0:s}".format(table_name))
            bbutil.log.exception(e)
            self.manager.abort()
            return False

        _res = True
        result = c.fetchone()
        if result is None:
            _res = False

        _check = self.manager.release()
        if _check is False:
            return False

        return _res

    def _count_table(self, table_name: str) -> int:
        c = self.manager.cursor()
        command = "SELECT count(*) FROM {0:s};".format(table_name)

        try:
            c.execute(command)
        except sqlite3.OperationalError as e:
            bbutil.log.error("Unable to count rows: {0:s}".format(table_name))
            bbutil.log.exception(e)
            self.manager.abort()
            return -1

        result = c.fetchall()
        (count,) = result[0]

        bbutil.log.debug1(self.name, "Count table: {0:s}, {1:d}".format(table_name, count))
        return count

    def count(self, table_name: str) -> int:
        _check = self.manager.connect()
        if _check is False:
            return -1

        _count = self._count_table(table_name)
        if _count == -1:
            return -1

        _check = self.manager.release()
        if _check is False:
            return -1

        return _count

    def _check_table(self, table_name: str) -> bool:
        _connection = self.manager.connection
        c = _connection.cursor()
        command = "SELECT name FROM sqlite_master WHERE type='table' AND name='{0:s}';".format(table_name)

        bbutil.log.debug1(self.name, "Check for table: {0:s}".format(table_name))

        try:
            c.execute(command)
        except sqlite3.OperationalError as e:
            bbutil.log.error("Unable to check for table: {0:s}".format(table_name))
            bbutil.log.exception(e)
            return False

        result = c.fetchone()
        if result is None:
            return False
        return True

    def prepare_table(self, table_name: str, column_list: list, unique_list: list, skip_check: bool = False) -> int:
        _check = self.manager.connect()
        if _check is False:
            return -1

        if skip_check is False:
            _check = self._check_table(table_name)
            if _check is True:
                _count = self._count_table(table_name)

                _check = self.manager.release()
                if _check is False:
                    return -1

                return _count

        _connection = self.manager.connection
        c = _connection.cursor()

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
            bbutil.log.error("Unable to create table: {0:s}".format(table_name))
            bbutil.log.exception(e)
            print(command)
            self.manager.abort()
            return -1

        bbutil.log.debug1(self.name, "Create table: {0:s}".format(table_name))

        _check = self.manager.commit()
        if _check is False:
            self.manager.release()
            return -1

        _check = self.manager.release()
        if _check is False:
            return -1
        return 0

    @staticmethod
    def _single_execute(table_name: str, names: list, data: Data) -> Optional[Execute]:
        _data = []
        _names = ", ".join(names)
        _placeholder = ", ".join(['?'] * len(names))

        sql = 'INSERT INTO "{0:s}" ({1:s}) VALUES ({2:s});'.format(table_name, _names, _placeholder)

        for _line in names:
            try:
                _value = getattr(data, _line)
            except AttributeError as e:
                bbutil.log.exception(e)
                bbutil.log.error("Data format does not fit database table!")
                return None
            _data.append(_value)
        _execute = Execute(sql=sql, data=_data)
        return _execute

    @staticmethod
    def _many_execute(table_name: str, names: list, data_list: List[Data]) -> Optional[Execute]:
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
                    bbutil.log.exception(e)
                    bbutil.log.error("Data format does not fit database table!")
                    return None
                _value.append(_ret)
            _data.append(_value)

        _execute = Execute(sql=sql, data=_data)
        return _execute

    def _insert(self, table_name: str, names: list, data: Union[Data, List[Data]]) -> int:
        c = self.manager.cursor()

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
            bbutil.log.exception(e)
            bbutil.log.error("One or more values is an invalid format!")
            bbutil.log.error("SQL:  " + str(_execute.sql))
            bbutil.log.error("DATA: " + str(_execute.data))
            return -1
        except OverflowError as e:
            bbutil.log.exception(e)
            bbutil.log.error("One or more values is too large!")
            bbutil.log.error("SQL:  " + str(_execute.sql))
            bbutil.log.error("DATA: " + str(_execute.data))
            return -1
        except sqlite3.IntegrityError:
            return -1
        except Exception as e:
            bbutil.log.exception(e)
            bbutil.log.error("SQL:  " + str(_execute.sql))
            bbutil.log.error("DATA: " + str(_execute.data))
            return -1

        _counter = c.rowcount

        if _counter > 0:
            _check = self.manager.commit()
            if _check is False:
                return -1

        return _counter

    @staticmethod
    def _get_chunk_size(max_intervall: int) -> int:
        interval = 1

        if max_intervall > 500:
            interval = 5

        if max_intervall > 1000:
            interval = 10

        if max_intervall > 5000:
            interval = 50

        if max_intervall > 10000:
            interval = 100

        if max_intervall > 20000:
            interval = 200

        if max_intervall > 50000:
            interval = 500

        return interval

    @staticmethod
    def _split_list(data_list: List[Data], chunk_size: int) -> list:
        chunked_list = []
        for i in range(0, len(data_list), chunk_size):
            chunked_list.append(data_list[i:i + chunk_size])

        return chunked_list

    def _insert_list(self, table_name: str, names: list, data_list: List[Data]) -> int:
        _chunk_size = self._get_chunk_size(len(data_list))
        _split_list = self._split_list(data_list, _chunk_size)
        _max = len(_split_list) + 1

        _progress = bbutil.log.progress(_max)

        _counter = 0
        _stored = 0

        for _item_list in _split_list:
            _counter += len(_item_list)
            _result = self._insert(table_name, names, _item_list)
            if _result == -1:
                bbutil.log.clear()
                return -1

            _stored += _result

            _progress.inc()

        bbutil.log.clear()

        if _counter != _stored:
            bbutil.log.warn(self.name, "Entries {0:d}, Stored {1:d}".format(_counter, _stored))
        else:
            bbutil.log.inform(self.name, "Stored {0:d}".format(_counter))

        return _stored

    def insert(self, table_name: str, names: list, data: Union[Data, List[Data]]) -> int:
        _check = self.manager.connect()
        if _check is False:
            return -1

        if type(data) is list:
            count = self._insert_list(table_name, names, data)
        else:
            count = self._insert(table_name, names, data)

        if count == -1:
            self.manager.abort()
            return -1

        _check = self.manager.release()
        if _check is False:
            return -1

        return count

    def update(self, table_name: str, names: list, data: Data, sql_filter: str, filter_value=None) -> bool:
        _check = self.manager.connect()
        if _check is False:
            return False

        c = self.manager.cursor()

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
            bbutil.log.error("SQL:  " + str(sql))
            bbutil.log.error("DATA: " + str(_data))
            bbutil.log.exception(e)
            return False
        except OverflowError as e:
            bbutil.log.exception(e)
            bbutil.log.error("SQL:  " + str(sql))
            bbutil.log.error("DATA: " + str(_data))
            return False

        _check = self.manager.commit()
        if _check is False:
            return False

        _check = self.manager.release()
        if _check is False:
            return False

        return True

    @staticmethod
    def _select_execute(cursor: sqlite3.Cursor, command: str, data: list):
        if len(data) == 0:
            cursor.execute(command)
        else:
            cursor.execute(command, data)
        return

    def select(self, table_name: str, names: list, sql_filter: str, data: list) -> Optional[list]:
        _check = self.manager.connect()
        if _check is False:
            return None

        c = self.manager.cursor()

        _selector = "*"
        if len(names) != 0:
            _selector = ", ".join(names)

        command = "SELECT {0:s} FROM {1:s};".format(_selector, table_name)

        if sql_filter != "":
            command = "SELECT {0:s} FROM {1:s} WHERE {2:s};".format(_selector, table_name, sql_filter)

        bbutil.log.debug1(table_name, command)

        try:
            self._select_execute(c, command, data)
        except sqlite3.OperationalError as e:
            bbutil.log.error("Unable to search table: {0:s}".format(table_name))
            bbutil.log.exception(e)
            bbutil.log.error("SQL:  " + str(command))
            bbutil.log.error("DATA: " + str(data))
            return None
        except OverflowError as e:
            bbutil.log.error("Unable to search table due to overflow: {0:s}".format(table_name))
            bbutil.log.exception(e)
            bbutil.log.error("SQL:  " + str(command))
            bbutil.log.error("DATA: " + str(data))
            return None

        _fetchlist = []

        for _data in c:
            _fetchlist.append(_data)

        _check = self.manager.release()
        if _check is False:
            return None

        return _fetchlist
