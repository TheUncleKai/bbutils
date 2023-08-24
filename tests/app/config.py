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
from tests.helper.config import MockArgumentParser

from testdata.app.config import AppConfig


__all__ = [
    "TestConfig"
]

oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()


class TestConfig(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser)
    def test_init_01(self):
        _config = AppConfig()

        _check = _config.init()
        self.assertTrue(_check)
        return
