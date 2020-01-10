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

import sys
import traceback
import time

from typing import List, Dict
from threading import Thread

from bbutil.types import Message, Timer, Progress, Writer

__all__ = [
    "types",
    "utils",

    "Logging"
]


#: package name
__name__ = "bblogging"

#: package author
__author__ = "Kai Raphahn"

#: email of package maintainer
__email__ = "kai.raphahn@laburec.de"

#: copyright year
__year__ = 2020

#: package copyright
__copyright__ = "Copyright (C) {0:d}, {1:s} <{2:s}>".format(__year__, __author__, __email__)

#: package description
__description__ = "Python tools for EASYBus Sensor modules from GMH Messtechnik GmbH"

#: package license
__license__ = "Apache License, Version 2.0"

#: package credits
__credits__ = [__author__]

#: version milestone
__milestone__ = 0

#: version major
__major__ = 0

#: version minor
__minor__ = 1

#: version patch
__patch__ = 0

#: package version
__version__ = "{0:d}.{1:d}.{2:d}.{3:d}".format(__milestone__, __major__, __minor__, __patch__)

#: package maintainer
__maintainer__ = __author__

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}


class Logging(object):

    def __init__(self):
        self._level: int = 0
        self._app: str = ""
        self._timer_list: List[Timer] = []
        self._timer_counter: int = 0

        self._buffer: List[Message] = []
        self._interval: float = 0.1
        self._active: bool = False
        self._index: Dict[int, List[str]] = {}
        self._thread: bool = False
        self._writer: List[Writer] = []
        return

    def __del__(self):
        self.close()
        return

    def _process(self, item: Message):
        for writer in self._writer:
            if (item.level not in writer.index) and (item.raw is False):
                continue
            writer.write(item)
        return

    def _run(self):

        while True:
            self._thread = True
            if self._active is False:
                self._thread = False
                break

            time.sleep(self._interval)
            count = len(self._buffer)

            if count == 0:
                continue

            _message = self._buffer.pop(0)
            self._process(_message)
        return

    def register(self, writer: Writer):
        self._writer.append(writer)
        return

    def append(self, item: Message):
        if self._level not in self._index:
            return

        level_list = self._index[self._level]

        if item.level not in level_list:
            return

        item.app = self._app
        self._buffer.append(item)
        return

    def setup(self, **kwargs):
        item = kwargs.get("app", None)
        if item is not None:
            self._app = item

        item = kwargs.get("interval", None)
        if item is not None:
            self._interval = item

        item = kwargs.get("level", None)
        if item is not None:
            self._level = item

        item = kwargs.get("index", None)
        if item is not None:
            self._index = item
        return

    def open(self) -> bool:
        if len(self._index) == 0:
            self._index = _index

        if self._thread is True:
            return True

        for item in self._writer:
            check = item.open()
            if check is False:
                return False

        self._active = True
        thread = Thread(target=self._run)
        thread.start()
        return True

    def close(self) -> bool:
        self._active = False

        if self._thread is False:
            return True

        while True:

            if self._thread is False:
                break
            time.sleep(0.01)

        for item in self._writer:
            check = item.close()
            if check is False:
                return False

        return True

    def inform(self, tag: str, content: str):
        _message = Message(tag=tag, content=content, level="INFORM")
        self._buffer.append(_message)
        return

    def warn(self, tag: str, content: str):
        _message = Message(tag=tag, content=content, level="WARN")
        self._buffer.append(_message)
        return

    def debug1(self, tag: str, content: str):
        _message = Message(tag=tag, content=content, level="DEBUG1")
        self._buffer.append(_message)
        return

    def debug2(self, tag: str, content: str):
        _message = Message(tag=tag, content=content, level="DEBUG2")
        self._buffer.append(_message)
        return

    def debug3(self, tag: str, content: str):
        _message = Message(tag=tag, content=content, level="DEBUG3")
        self._buffer.append(_message)
        return

    def error(self, content: str):
        _message = Message(content=content, level="ERROR")
        self._buffer.append(_message)
        return

    def exception(self, e: Exception):
        content = "An exception of type {0} occurred.".format(type(e).__name__)
        _message = Message(content=content, level="EXCEPTION")
        self._buffer.append(_message)

        content = "Arguments:\n{0!r}".format(e.args)
        _message = Message(content=content, level="EXCEPTION")
        self._buffer.append(_message)
        return

    def traceback(self):

        ttype, value, tb = sys.exc_info()
        self.error("Uncaught exception")
        self.error("Type:  " + str(ttype))
        self.error("Value: " + str(value))

        lines = traceback.format_tb(tb)
        for line in lines:
            _message = Message(content=line, raw=True)
            self._buffer.append(_message)
        return

    def progress(self, limit: int, interval: int = 0) -> Progress:
        _progress = Progress(limit, interval, self.append)
        return _progress

    def timer(self, content: str) -> Timer:
        _timer = Timer(content, self.append)
        return _timer
