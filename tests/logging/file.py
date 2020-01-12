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

import time
import sys
import os
import unittest
import unittest.mock as mock

from bbutil.logging.writer.file import FileWriter
from bbutil.logging.types import Message, Progress, Writer


class Callback(object):

    def __init__(self, writer: Writer):
        self.item = None
        self.writer = writer
        return

    def append(self, item: Message):
        self.writer.write(item)
        return


class SysWrite(mock.MagicMock):

    encoding = "cp850"

    def __index__(self):
        mock.MagicMock.__init__(self)
        return


class TestConsoleWriter(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_constructor(self):

        item = FileWriter()
        self.assertEqual(item.filename, "")
        self.assertEqual(item.text_space, 15)
        self.assertIsNone(item.file)
        self.assertFalse(item.append_data)
        return

    def test_setup_01(self):

        item = FileWriter()
        item.setup(text_space=20, filename="run-tests.log", append_data=True)
        print(item.filename)

        self.assertNotEqual(item.filename, "")
        self.assertEqual(item.text_space, 20)
        self.assertIsNone(item.file)
        self.assertTrue(item.append_data)
        return

    def test_setup_02(self):

        item = FileWriter()
        item.setup(text_space=20, logname="run-tests", logpath=os.getcwd(), append_datetime=True)
        print(item.filename)

        self.assertNotEqual(item.filename, "")
        self.assertEqual(item.text_space, 20)
        self.assertIsNone(item.file)
        self.assertFalse(item.append_data)
        return

    def test_setup_03(self):

        args = {
            "text_space": 20,
            "logname": "",
            "logpath": os.getcwd(),
            "append_datetime": True
        }

        item = FileWriter()
        self.assertRaises(ValueError, item.setup, **args)
        return

    def test_clear(self):

        item = FileWriter()
        item.clear()
        return

    mocked_open = unittest.mock.mock_open(read_data='file contents\nas needed\n')

    mocked_open_fail1 = unittest.mock.mock_open()
    mocked_open_fail1.side_effect = OSError(5)

    mocked_open_fail2 = unittest.mock.mock_open()
    mocked_open_fail2.side_effect = ValueError("Invalid param")

    @mock.patch('builtins.open', new=mocked_open)
    def test_open_01(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        check = item.open()

        self.assertIsNotNone(item.file)
        self.assertTrue(check)
        return

    @mock.patch('builtins.open', new=mocked_open_fail1)
    def test_open_02(self):
        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        check = item.open()

        self.assertIsNone(item.file)
        self.assertFalse(check)
        return

    @mock.patch('builtins.open', new=mocked_open_fail2)
    def test_open_03(self):
        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        check = item.open()

        self.assertIsNone(item.file)
        self.assertFalse(check)
        return

    def test_open_04(self):
        item = FileWriter()
        item.setup(text_space=20)

        self.assertRaises(ValueError, item.open)
        return
