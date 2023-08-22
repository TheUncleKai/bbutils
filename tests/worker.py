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

import os
import unittest

import unittest.mock as mock

from bbutil.utils import full_path

from tests.helper import set_log
from tests.helper.worker import Worker01

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
        _worker = Worker01(id="Worker01", use_thread=True)

        _check = _worker.execute()
        self.assertTrue(_check)
        self.assertFalse(_worker.error)
        return

    def test_worker_03(self):
        _worker = Worker01(id="Worker01", exit_prepare=False)

        _check = _worker.execute()
        self.assertFalse(_check)
        self.assertTrue(_worker.error)
        return
