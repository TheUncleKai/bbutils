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
import threading
import time
from abc import ABCMeta
from dataclasses import dataclass

import bbutil
from bbutil.worker.callback import Callback

__all__ = [
    "Worker",

    "callback"
]


@dataclass
class Worker(metaclass=ABCMeta):

    id: str = ""
    abort: bool = True
    interval: float = 0.01
    use_thread: bool = False

    _callback: Callback = Callback()
    _error: bool = True
    _running: bool = True

    @property
    def error(self) -> bool:
        return self._error

    @abc.abstractmethod
    def prepare(self) -> bool:
        pass

    @abc.abstractmethod
    def run(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self) -> bool:
        pass

    def set_callback(self, **kwargs):
        self._callback.set_callback(**kwargs)
        return

    def _do_step(self, step: str, function, callback_func):
        if self.abort is True:
            self.abort = False
            return

        callback_func()

        _check = function()
        if _check is False:
            self._error = True
            bbutil.log.error("{0:s}: {1:s} failed!".format(self.id, step))
        return

    def _execute(self):
        self._running = True
        self._callback.do_start()

        self._do_step("prepare", self.prepare, self._callback.do_prepare)
        if self._error is True:
            self._running = False
            return

        self._do_step("run", self.run, self._callback.do_run)
        if self._error is True:
            self._running = False
            return

        self._do_step("close", self.close, self._callback.do_close)

        self._callback.do_close()
        self._running = False
        return

    def execute(self) -> bool:

        if self.use_thread is False:
            self._execute()
            return self._error

        _t = threading.Thread(target=self._execute)

        _t.start()
        _run = True

        while _run is True:
            time.sleep(self.interval)

            if self._running is False:
                _run = False

        return self._error
