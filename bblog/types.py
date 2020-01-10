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
from datetime import datetime

__all__ = [
    "Message",
    "Timer",
    "Progress"
]


class Message(object):

    def __init__(self, **kwargs):
        self.time = datetime.now()
        self.app: str = ""
        self.tag: str = ""
        self.content: str = ""
        self.level: str = ""
        self.raw: bool = False

        self.counter: int = 0
        self.limit: int = 0
        self.value: float = 0

        item = kwargs.get("app", None)
        if item is not None:
            self.app = item

        item = kwargs.get("tag", None)
        if item is not None:
            self.tag = item

        item = kwargs.get("level", None)
        if item is not None:
            self.level = item

        item = kwargs.get("content", None)
        if item is not None:
            self.content = item

        item = kwargs.get("raw", None)
        if item is not None:
            self.raw = item

        item = kwargs.get("progress", None)
        if item is not None:
            self.progress = item

        item = kwargs.get("counter", None)
        if item is not None:
            self.counter = item

        item = kwargs.get("limit", None)
        if item is not None:
            self.limit = item

        item = kwargs.get("value", None)
        if item is not None:
            self.value = item
        return


class Timer(object):

    def __init__(self, content: str, append_callback):
        self.content: str = content
        self.start: datetime = datetime.now()
        self._append = append_callback
        return

    def stop(self):
        delta = datetime.now() - self.start
        content = "Runtime: {0:s} for {1:s}".format(str(delta), self.content)

        _message = Message(content=content, level="TIMER")
        self._append(_message)
        return


class Progress(object):

    def __init__(self, limit: int, interval: int, append_callback):
        self._limit: int = limit
        self._counter: int = 0
        self._value: float = 0.0
        self._finished: bool = False
        self._interval: int = interval
        self._interval_counter: int = 10
        self._append = append_callback
        return

    def _recalc(self):
        """recalculate progress.
        """
        self._value = float(self._counter) * 100.0 / float(self._limit)

        if self._interval != 0:
            self._interval_counter += 1
            if self._interval_counter == self._interval:
                self._interval_counter = 0

        if self._counter == self._limit:
            self._finished = True
        return

    def inc(self):
        self._counter += 1

        self._recalc()

        _message = Message(level="PROGRESS", limit=self._limit, counter=self._counter, value=self._value)
        self._append(_message)
        return

    def dec(self):
        self._counter += 1

        self._recalc()

        if self._interval_counter != 0:
            return

        _message = Message(level="PROGRESS", limit=self._limit, counter=self._counter, value=self._value)
        self._append(_message)
        return
