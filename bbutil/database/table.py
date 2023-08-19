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

import sys

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from bbutil.logging import Logging

from bbutil.database import Column, Types, Data, DataType, select_interval
from bbutil.database.sqlite import SQLite


__all__ = [
    "Table"
]


@dataclass
class Table(object):

    log: Optional[Logging] = None

    name: str = ""
    counter: int = 0
    keyword: str = ""
    sqlite: Optional[SQLite] = None
    data: List[Data] = field(default_factory=list)
    index: Dict[Any, List[Data]] = field(default_factory=dict)
    columns: List[Column] = field(default_factory=list)
    _datacolumns: List[str] = field(default_factory=list)

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
            self._datacolumns.append(name)
        return

    def select(self, data_filter: str = "", data_values=None, warn: bool = False, verbose: bool = False) -> List[Data]:
        if data_values is None:
            data_values = []

        _result = []

        _data_list = self.sqlite.select(table_name=self.name, sql_filter=data_filter, names=[], data=data_values)
        if _data_list is None:
            if warn is True:
                self.log.warn(self.name, "No data!")
            return _result

        _count = len(_data_list)
        if _count == 0:
            if warn is True:
                self.log.warn(self.name, "No data!")
            return _result

        if verbose is True:
            self.log.inform("Table", "Load {0:d} from {1:s}".format(_count, self.name))

        progress = self.log.progress(_count, select_interval(_count))

        for _data in _data_list:
            _number = 0

            key_list = []
            value_list = []

            for _col in self.columns:
                _value = _data[_number]

                key_list.append(_col.name)
                value_list.append(_value)
                _number += 1

            _entry = Data(keys=key_list, values=value_list)
            _result.append(_entry)
            if verbose is True:
                progress.inc()

        if verbose is True:
            self.log.clear()
        return _result

    def select_all(self) -> List[Data]:
        _result = []

        _data_list = self.sqlite.select(table_name=self.name, sql_filter="", names=[], data=[])
        if _data_list is None:
            self.log.warn(self.name, "No data!")
            return _result

        _count = len(_data_list)
        if _count == 0:
            self.log.warn(self.name, "No data!")
            return _result

        self.log.inform("Table", "Load {0:d} from {1:s}".format(_count, self.name))
        progress = self.log.progress(_count, select_interval(_count))

        _count = 0
        for _data in _data_list:
            _number = 0

            key_list = []
            value_list = []

            for _col in self.columns:
                try:
                    _value = _data[_number]
                except IndexError as e:
                    self.log.error("Problem with data item {0:d}!".format(_count))
                    self.log.error("Column {0:d} ({1:s}) not found!".format(_number, _col.name))
                    self.log.exception(e)
                    print(_data)
                    sys.exit(1)

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
            progress.inc()

        self.log.clear()
        return _result

    def store_item(self, data: Data) -> bool:
        _check = self.sqlite.insert(self.name, self._datacolumns, data)
        return _check

    def old_store(self) -> int:
        _ret = self.sqlite.insertmany(self.name, self._datacolumns, self.data)
        return _ret

    @staticmethod
    def _split_list(data_list: List[Data], chunk_size: int) -> list:
        chunked_list = []
        for i in range(0, len(data_list), chunk_size):
            chunked_list.append(data_list[i:i + chunk_size])

        return chunked_list

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

    def store(self) -> int:
        _chunk_size = self._get_chunk_size(len(self.data))
        _split_list = self._split_list(self.data, _chunk_size)
        _max = len(_split_list) + 1
        _progress = self.log.progress(_max)

        _counter = 0
        _stored = 0

        for _item_list in _split_list:
            _counter += len(_item_list)
            _stored += self.sqlite.insertmany(self.name, self._datacolumns, _item_list)
            _progress.inc()

        self.log.clear()
        if _counter != _stored:
            self.log.warn(self.name, "Entries {0:d}, Stored {1:d}".format(_counter, _stored))
        else:
            self.log.inform(self.name, "Stored {0:d}".format(_counter))

        return _stored

    def update(self, data: Data, data_filter: str, filter_value=None) -> bool:
        _check = self.sqlite.update(self.name, self._datacolumns, data, data_filter, filter_value)
        return _check

    def init(self) -> bool:

        if len(self.columns) == 0:
            self.log.error("No columns: {0:s}".format(self.name))
            return False

        _columns = []
        for _col in self.columns:
            _columns.append(_col.create)

        _unique = []
        for _col in self.columns:
            if _col.unique is False:
                continue
            _unique.append(_col.name)

        _check = self.sqlite.prepare_table(self.name, _columns, _unique)
        if _check is False:
            return False

        self.counter = self.sqlite.count_table(self.name)
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

    def load(self, **kwargs):
        self.log.inform("Data", "Load {0:s}...".format(self.name))

        _all = kwargs.get("all", False)

        if _all is True:
            _items = self.select_all()
        else:
            _items = self.select(**kwargs)

        _max = len(_items) + 1
        _progress = self.log.progress(_max, select_interval(_max))

        for _item in _items:
            self.add(_item)
            _progress.inc()
        self.log.clear()
        return
