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
from bbutil.execute import Execute

from tests.helper import set_log

__all__ = [
    "TestExecute"
]

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
            "/usr/bin/ls"
        ]

        _execute.setup(name="Test", desc="Print ls", commands=_commands)

        _check = _execute.execute()
        self.assertTrue(_check)
        self.assertEqual(_execute.returncode, 0)
        self.assertIsNone(_execute.errors)
        self.assertGreater(len(_execute.messages), 1)
        return
