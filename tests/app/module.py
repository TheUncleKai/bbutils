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

from bbutil.app.module import Module

__all__ = [
    "TestModule"
]

oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()


class TestModule(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_init_01(self):
        _module = Module()

        _path = "testdata.commands"
        _name = "testone"
        _check1 = _module.init(_path, _name)

        self.assertTrue(_check1)
        self.assertEqual(_module.command, "test01")
        self.assertEqual(_module.desc, "the first test")
        return

    def test_init_02(self):
        _module = Module()

        _path = "testdata.commands"
        _name = "testonex"
        _check1 = _module.init(_path, _name)

        self.assertFalse(_check1)
        return
