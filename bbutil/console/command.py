#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import abc
import time

from dataclasses import dataclass
from abc import ABCMeta
from typing import List

import mig

from mig.base.worker import Worker


__all__ = [
    "Command"
]


@dataclass
class Command(metaclass=ABCMeta):

    name: str = ""

    @staticmethod
    def inform(name: str, data: str):
        tag = str(name).ljust(20, " ")
        line = "{0:s}: {1:s}".format(tag, data)
        mig.log.inform(mig.module.name, line)
        return

    @staticmethod
    def warn(name: str, data: str):
        tag = str(name).ljust(20, " ")
        line = "{0:s}: {1:s}".format(tag, data)
        mig.log.warn(mig.module.name, line)
        return

    @staticmethod
    def run_worker(worker: List[Worker]) -> bool:

        for _worker in worker:
            _check = _worker.execute()
            if _check is False:
                mig.log.error("{0:s} failed!".format(_worker.worker_id))
                return False
        return True

    @staticmethod
    def run_thread(t) -> bool:
        t.start()

        _run = True

        while _run is True:
            time.sleep(0.01)

            if t.is_running is False:
                _run = False

        if t.success is False:
            return False
        return True

    @abc.abstractmethod
    def prepare(self) -> bool:
        pass

    @abc.abstractmethod
    def run(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self) -> bool:
        pass

    def execute(self) -> int:

        _check = mig.data.start()
        if _check is False:
            return False

        ret = 0
        try:
            if self.prepare() is False:
                ret = 1

            if ret == 0:
                if self.run() is False:
                    ret = 2

            if ret == 0:
                if self.close() is False:
                    ret = 3

        except Exception as e:
            ret = 4
            mig.log.exception(e)
            mig.log.traceback()

        _check = mig.data.stop()
        if _check is False:
            return ret

        return ret
