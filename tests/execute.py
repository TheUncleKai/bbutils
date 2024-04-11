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

import unittest.mock as mock

from bbutil.execute import Execute

from tests.helper import set_log
from tests.helper.execute import CatchBacks, MockPopen1, MockPopen2, MockPopen3

__all__ = [
    "TestExecute"
]


if sys.platform == "win32":
    _ls = "dir.bat"
    _param = "/L"
else:
    _ls = "/usr/bin/ls"
    _param = "-lA"


oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()


class TestExecute(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_setup_01(self):
        _execute = Execute()

        _commands = [
            _ls
        ]

        print(_commands)

        _execute.setup(name="Test", desc="Print ls", commands=_commands)

        _check = _execute.execute()
        self.assertTrue(_check)
        self.assertEqual(_execute.returncode, 0)
        self.assertIsNone(_execute.errors)
        self.assertGreater(len(_execute.messages), 1)
        return

    def test_setup_02(self):
        _commands = [
            _ls
        ]

        _execute = Execute(name="Test", desc="Print ls", commands=_commands)

        _check = _execute.execute()
        self.assertTrue(_check)
        self.assertEqual(_execute.returncode, 0)
        self.assertIsNone(_execute.errors)
        self.assertGreater(len(_execute.messages), 1)
        return

    @mock.patch('subprocess.Popen', new=MockPopen1)
    def test_setup_03(self):

        _execute = Execute()
        _commands = [
            _ls,
            _param
        ]

        _execute.setup(name="Test", desc="Print ls", commands=_commands, stdout="TEST", stderr="TEST", stdin="TEST")
        _execute.show_command()

        _check = _execute.execute()
        self.assertTrue(_check)
        self.assertEqual(_execute.returncode, 0)
        self.assertIsNone(_execute.errors)
        self.assertGreater(len(_execute.messages), 1)
        return

    @mock.patch('subprocess.Popen', new=MockPopen2)
    def test_setup_04(self):

        _callbacks = CatchBacks()

        _execute = Execute()
        _commands = [
            _ls
        ]

        _execute.setup(name="Test", desc="Print ls", commands=_commands,
                       call_stdout=_callbacks.add_stdout, call_stderr=_callbacks.add_stderr)

        _check = _execute.execute()

        self.assertFalse(_check)
        self.assertEqual(_execute.returncode, 1)
        self.assertIsNotNone(_execute.errors)
        self.assertGreater(len(_execute.messages), 1)
        self.assertEqual(len(_callbacks.stdout), 22)
        self.assertEqual(len(_callbacks.stderr), 11)
        return

    @mock.patch('subprocess.Popen', new=MockPopen3)
    def test_setup_05(self):

        _callbacks = CatchBacks()

        _execute = Execute()
        _commands = [
            _ls
        ]

        _execute.setup(name="Test", desc="Print ls", commands=_commands,
                       call_stdout=_callbacks.add_stdout, call_stderr=_callbacks.add_stderr)

        _check = _execute.execute()

        self.assertFalse(_check)
        self.assertEqual(_execute.returncode, 1)
        self.assertIsNone(_execute.errors)
        self.assertGreater(len(_execute.messages), 1)
        self.assertEqual(len(_callbacks.stdout), 22)
        self.assertEqual(len(_callbacks.stderr), 0)
        return
