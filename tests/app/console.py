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
import unittest

from unittest.mock import patch, Mock

from tests.helper.console import AppConsole


__all__ = [
    "TestConsole"
]

oserror = OSError("Something strange did happen!")
mock_oserror = Mock(side_effect=oserror)
mock_remove = Mock()


class TestConsole(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        return

    def test_setup_01(self):
        _console = AppConsole()

        _check = _console.setup()
        self.assertTrue(_check)
        return

    def test_setup_02(self):
        _console = AppConsole()
        _console.module_path = "testdata.app.xcommands"

        _check = _console.setup()
        self.assertFalse(_check)
        return

    def test_setup_03(self):
        _console = AppConsole()
        _console.filename = "fuhhhhhhh"

        _check = _console.setup()
        self.assertFalse(_check)
        return

    def test_setup_04(self):
        _console = AppConsole()
        _console.module_path = ""

        _check = _console.setup()
        self.assertFalse(_check)
        return

    def test_execute_01(self):
        _console = AppConsole()

        _argv = [
            "run-tests.py",
            "test01"
        ]

        _check1 = _console.setup()

        with patch("sys.argv", _argv):
            _ret = _console.execute()

        self.assertTrue(_check1)
        self.assertEqual(_ret, 0)
        return