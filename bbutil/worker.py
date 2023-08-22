#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import time
import abc
import threading

from dataclasses import dataclass
from abc import ABCMeta

import bbutil


__all__ = [
    "Worker"
]


@dataclass
class _Callback(object):

    start = None
    stop = None
    prepare = None
    run = None
    close = None
    abort = None

    def do_start(self):
        if self.start is None:
            return
        self.start()
        return

    def do_stop(self):
        if self.stop is None:
            return
        self.start()
        return

    def do_prepare(self):
        if self.prepare is None:
            return
        self.start()
        return

    def do_run(self):
        if self.run is None:
            return
        return

    def do_close(self):
        if self.close is None:
            return
        return

    def do_abort(self):
        if self.abort is None:
            return
        return

@dataclass
class Worker(metaclass=ABCMeta):

    id: str = ""
    abort: bool = True
    interval: float = 0.01
    use_thread: bool = False

    _callback: _Callback = _Callback()
    _error: bool = True
    _running: bool = True

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
        _value = kwargs.get("start", None)
        if _value is not None:
            self._callback.start = _value

        _value = kwargs.get("stop", None)
        if _value is not None:
            self._callback.stop = _value

        _value = kwargs.get("start", None)
        if _value is not None:
            self._callback.prepare = _value

        _value = kwargs.get("start", None)
        if _value is not None:
            self._callback.run = _value

        _value = kwargs.get("start", None)
        if _value is not None:
            self._callback.close = _value
        return

    def _do_step(self, step: str, function, callback):
        if self.abort is True:
            self.abort = False
            return

        callback()

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
