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
#    Copyright (C) 2023, Kai Raphahn <kai.raphahn@laburec.de>
#

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum

import bbutil

from bbutil.database import Column, Types, Data, DataType, select_interval
from bbutil.database.sqlite import SQLite


__all__ = [
    "Table"
]


class _InitType(Enum):

    has_table = 0
    has_old_table = 1
    has_no_table = 2


@dataclass
class Table(object):

    name: str = ""
    old_name: str = ""
    _counter: int = 0
    keyword: str = ""
    sqlite: Optional[SQLite] = None
    data: List[Data] = field(default_factory=list)
    index: Dict[Any, List[Data]] = field(default_factory=dict)
    columns: List[Column] = field(default_factory=list)
    drop: List[str] = field(default_factory=list)
    names: List[str] = field(default_factory=list)
    suppress_warnings: bool = False

    def clear(self):
        self.data.clear()
        self.index.clear()
        return

    @property
    def data_count(self) -> int:
        _counter = len(self.data)
        return _counter

    def check(self) -> int:
        self._counter = self.sqlite.count(self.name)
        return self._counter

    @property
    def column_list(self) -> list:
        _columns = []
        for _col in self.columns:
            _columns.append(_col.create)
        return _columns

    @property
    def unique_list(self) -> list:
        _unique = []
        for _col in self.columns:
            if _col.unique is False:
                continue
            _unique.append(_col.name)
        return _unique

    def new_data(self) -> Data:
        key_list = []
        value_list = []

        for _column in self.columns:
            # noinspection PyTypeChecker
            _datatype: DataType = _column.type.value

            key_list.append(_column.name)
            value_list.append(_datatype.value)

        _data = Data(keys=key_list, values=value_list)
        return _data

    def add_column(self, name: str, data_type: Types, unique: bool = False, primarykey: bool = False,
                   keyword: bool = False):
        for _column in self.columns:
            if _column.name == name:
                return

        _column = Column(name=name, primarykey=primarykey, type=data_type, unique=unique)
        self.columns.append(_column)

        if keyword is True:
            self.keyword = name

        if primarykey is False:
            self.names.append(name)
        return

    def get_column(self, name: str) -> Optional[Column]:
        for _column in self.columns:
            if _column.name == name:
                return _column
        return None

    def drop_column(self, name: str) -> bool:
        _columns: List[Column] = []
        _names: List[str] = []
        _drop: Optional[Column] = self.get_column(name)

        if _drop is None:
            bbutil.log.error("Column {0:s} not found!".format(name))
            return False

        if _drop.primarykey is True:
            bbutil.log.error("Unable to drop primary key column!")
            return False

        if self.keyword == name:
            self.keyword = ""

        for _column in self.columns:
            if _column.name == name:
                self.drop.append(name)
                continue

            _columns.append(_column)
            _names.append(_column.name)

        self.columns = _columns
        self.names = _names
        return True

    def _process_datalist(self, data_list: List[Tuple], verbose: bool = True) -> Optional[List[Data]]:
        if data_list is None:
            if (self.suppress_warnings is False) and (verbose is True):
                bbutil.log.warn(self.name, "No data!")
            return None

        _count = len(data_list)
        if _count == 0:
            if (self.suppress_warnings is False) and (verbose is True):
                bbutil.log.warn(self.name, "No data!")
            return None

        progress = None
        if verbose is True:
            bbutil.log.inform("Table", "Load {0:d} from {1:s}".format(_count, self.name))
            progress = bbutil.log.progress(_count, select_interval(_count))

        _result = []
        _count = 0
        for _data in data_list:
            _number = 0

            key_list = []
            value_list = []

            for _col in self.columns:
                try:
                    _value = _data[_number]
                except IndexError as e:
                    bbutil.log.error("Problem with data item {0:d}!".format(_count))
                    bbutil.log.error("Column {0:d} ({1:s}) not found!".format(_number, _col.name))
                    bbutil.log.exception(e)
                    return None

                key_list.append(_col.name)

                if _col.type is Types.bool:
                    if _value == 1:
                        _value = True
                    else:
                        _value = False

                value_list.append(_value)
                _number += 1

            _count += 1

            _entry = Data(keys=key_list, values=value_list)
            _result.append(_entry)

            if progress is not None:
                progress.inc()

        if verbose is True:
            bbutil.log.clear()
        return _result

    def select(self, sql_filter: str = "", names=None, data_values=None, verbose: bool = True) -> List[Data]:
        if names is None:
            names = []

        if data_values is None:
            data_values = []

        _data_list = self.sqlite.select(table_name=self.name, sql_filter=sql_filter, names=names, data=data_values)
        _result = self._process_datalist(_data_list, verbose)

        if _result is None:
            return []

        return _result

    def store(self, data: Data = None) -> int:
        _data = data
        if data is None:
            _data = self.data

        _count = self.sqlite.insert(self.name, self.names, _data)
        return _count

    def update(self, data: Data, data_filter: str, filter_value=None) -> bool:
        _check = self.sqlite.update(self.name, self.names, data, data_filter, filter_value)
        return _check

    def _check_table(self) -> _InitType:
        _type = _InitType.has_no_table

        _check = self.sqlite.check_table(self.name)
        if _check is True:
            _type = _InitType.has_table
        else:

            if self.old_name != "":
                _check = self.sqlite.check_table(self.old_name)
                if _check is True:
                    _type = _InitType.has_old_table

        return _type

    def _create_table(self) -> bool:
        if len(self.columns) == 0:
            bbutil.log.error("No columns: {0:s}".format(self.name))
            return False

        _columns = []
        for _col in self.columns:
            _columns.append(_col.create)

        _unique = []
        for _col in self.columns:
            if _col.unique is False:
                continue
            _unique.append(_col.name)

        _check = self.sqlite.create_table(self.name, _columns, _unique)
        if _check is False:
            return False
        return True

    def _rename_table(self) -> bool:
        _check = self.sqlite.rename_table(self.old_name, self.name)
        if _check is False:
            return False
        return True

    def init(self) -> bool:
        if bbutil.log is None:
            return False

        self.sqlite.prepare()

        _type = self._check_table()

        _check = False

        if _type is _InitType.has_no_table:
            _check = self._create_table()

        if _type is _InitType.has_old_table:
            _check = self._rename_table()

        if _check is False:
            return False

        _count = self.sqlite.count(self.name)
        if _count == -1:
            return False

        self._counter = _count
        return True

    def add(self, item: Data):
        self.data.append(item)

        if self.keyword == "":
            return

        _keyword = getattr(item, self.keyword, None)
        if _keyword is None:
            raise Exception("Keyword is missing!")

        try:
            _list = self.index[_keyword]
        except KeyError:
            self.index[_keyword] = []
            _list = self.index[_keyword]

        _list.append(item)
        return

    def check_scheme(self) -> bool:
        if bbutil.log is None:
            return False

        if len(self.columns) == 0:
            bbutil.log.error("No columns: {0:s}".format(self.name))
            return False

        _scheme = {}

        _data = self.sqlite.get_scheme(self.name)
        if _data is None:
            bbutil.log.error("Scheme for {0:s} not found!".format(self.name))
            return False

        for item in _data:
            _scheme[item[0]] = item[1]

        for _column in self.columns:
            try:
                _value = _scheme[_column.name]
            except KeyError:
                bbutil.log.error("Column {0:s} in {1:s} not found!".format(_column.name, self.name))
                return False

            expected_value = _column.type.value.type

            if expected_value != _value:
                _error = "Column {0:s} in {1:s} does not match: found {2:s}, expected {3:s}".format(_column.name,
                                                                                                    self.name,
                                                                                                    _value,
                                                                                                    expected_value)
                bbutil.log.error(_error)
                return False
        return True

    def load(self) -> int:
        bbutil.log.inform(self.name, "Load {0:s}...".format(self.name))

        _items = self.select()
        _count = len(_items)

        _max = _count + 1
        _progress = bbutil.log.progress(_max, select_interval(_max))

        for _item in _items:
            self.add(_item)
            _progress.inc()

        bbutil.log.clear()

        _count = self.data_count
        return _count
