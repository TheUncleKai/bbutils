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

import unittest.mock as mock

from tests.helper import set_log
from tests.helper.worker import Worker01, Worker02

__all__ = [
    "TestWorker"
]

oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()


class TestWorker(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_worker_01(self):
        _worker = Worker01(id="Worker01")

        _check = _worker.execute()
        self.assertTrue(_check)
        self.assertFalse(_worker.error)
        return

    def test_worker_02(self):
        _worker = Worker01(id="Worker01")

        _worker.start()
        _worker.wait()

        self.assertFalse(_worker.error)
        return

    def test_worker_03(self):
        _worker = Worker01(id="Worker01", exit_prepare=False)

        _check = _worker.execute()
        self.assertFalse(_check)
        self.assertTrue(_worker.error)
        return

    def test_worker_04(self):
        _worker = Worker01(id="Worker01", exit_run=False)

        _check = _worker.execute()
        self.assertFalse(_check)
        self.assertTrue(_worker.error)
        return

    def test_worker_05(self):
        _worker = Worker01(id="Worker01", exit_close=False)

        _check = _worker.execute()
        self.assertFalse(_check)
        self.assertTrue(_worker.error)
        return

    def test_worker_06(self):
        _worker = Worker01(id="Worker01")

        _worker.start()
        _check = _worker.is_running
        _worker.wait()

        self.assertTrue(_check)
        self.assertFalse(_worker.error)
        return

    def test_worker_07(self):
        _worker = Worker02(id="Worker02")

        _worker.start()
        _check1 = _worker.is_running
        _worker.abort = True

        _worker.wait()
        self.assertFalse(_worker.error)
        return
