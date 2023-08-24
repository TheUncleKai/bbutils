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

import unittest
import time

from tests.helper import set_log
from tests.helper.worker import CallManager, Worker01, Worker02

__all__ = [
    "TestWorker"
]


class TestWorker(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_worker_01(self):
        _worker = Worker01()

        _check = _worker.execute()
        self.assertEqual(_worker.id, "Worker01")
        self.assertTrue(_check)
        self.assertFalse(_worker.error)
        return

    def test_worker_02(self):
        _calls = CallManager()
        _worker = Worker01()
        _calls.setup(_worker)

        _worker.start()
        _worker.wait()

        self.assertFalse(_worker.error)

        _calls.info()
        self.assertEqual(_calls.start, 1)
        self.assertEqual(_calls.stop, 1)
        self.assertEqual(_calls.prepare, 1)
        self.assertEqual(_calls.run, 1)
        self.assertEqual(_calls.close, 1)
        self.assertEqual(_calls.abort, 0)
        return

    def test_worker_03(self):
        _calls = CallManager()
        _worker = Worker01(exit_prepare=False)
        _calls.setup(_worker)

        _check = _worker.execute()
        self.assertFalse(_check)
        self.assertTrue(_worker.error)

        _calls.info()
        self.assertEqual(_calls.start, 1)
        self.assertEqual(_calls.stop, 1)
        self.assertEqual(_calls.prepare, 1)
        self.assertEqual(_calls.run, 0)
        self.assertEqual(_calls.close, 0)
        self.assertEqual(_calls.abort, 0)
        return

    def test_worker_04(self):
        _calls = CallManager()
        _worker = Worker01(exit_run=False)
        _calls.setup(_worker)

        _check = _worker.execute()
        self.assertFalse(_check)
        self.assertTrue(_worker.error)

        _calls.info()
        self.assertEqual(_calls.start, 1)
        self.assertEqual(_calls.stop, 1)
        self.assertEqual(_calls.prepare, 1)
        self.assertEqual(_calls.run, 1)
        self.assertEqual(_calls.close, 0)
        self.assertEqual(_calls.abort, 0)
        return

    def test_worker_05(self):
        _calls = CallManager()
        _worker = Worker01(exit_close=False)
        _calls.setup(_worker)

        _check = _worker.execute()
        self.assertFalse(_check)
        self.assertTrue(_worker.error)

        _calls.info()
        self.assertEqual(_calls.start, 1)
        self.assertEqual(_calls.stop, 1)
        self.assertEqual(_calls.prepare, 1)
        self.assertEqual(_calls.run, 1)
        self.assertEqual(_calls.close, 1)
        self.assertEqual(_calls.abort, 0)
        return

    def test_worker_06(self):
        _calls = CallManager()
        _worker = Worker01()
        _calls.setup(_worker)

        _worker.start()
        _worker.wait()

        self.assertFalse(_worker.error)

        _calls.info()
        self.assertEqual(_calls.start, 1)
        self.assertEqual(_calls.stop, 1)
        self.assertEqual(_calls.prepare, 1)
        self.assertEqual(_calls.run, 1)
        self.assertEqual(_calls.close, 1)
        self.assertEqual(_calls.abort, 0)
        return

    def test_worker_07(self):
        _calls = CallManager()
        _worker = Worker02(max=250000)
        _calls.setup(_worker)

        _worker.start()
        _check1 = _worker.is_running
        time.sleep(1)
        _worker.abort = True

        _worker.wait()
        self.assertFalse(_worker.error)

        _calls.info()
        self.assertEqual(_calls.start, 1)
        self.assertEqual(_calls.stop, 1)
        self.assertEqual(_calls.prepare, 1)
        self.assertEqual(_calls.run, 0)
        self.assertEqual(_calls.close, 0)
        self.assertEqual(_calls.abort, 1)
        return

    def test_worker_08(self):
        _worker = Worker02(max=250000)

        _worker.start()
        _check1 = _worker.is_running
        _worker.abort = True

        _worker.wait()
        self.assertFalse(_worker.error)
        return
