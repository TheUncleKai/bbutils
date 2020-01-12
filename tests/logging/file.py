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

from bbutil.logging.writer.file import FileWriter
from bbutil.logging.types import Message, Writer

mocked_open1 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_open2 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_open2.side_effect = OSError(5)

mocked_open3 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_open3.side_effect = ValueError(5)

mocked_open4 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_open5 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_open6 = unittest.mock.mock_open(read_data='file contents\nas needed\n')

mocked_write1 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_write2 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_write3 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_write4 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_write5 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_write6 = unittest.mock.mock_open(read_data='file contents\nas needed\n')
mocked_write7 = unittest.mock.mock_open(read_data='file contents\nas needed\n')

mocked_close1 = unittest.mock.mock_open(read_data='file contents\nas needed\n')

# mocked_open_fail1 = unittest.mock.mock_open()
# mocked_open_fail1.side_effect = OSError(5)
#
# mocked_open_fail2 = unittest.mock.mock_open()
# mocked_open_fail2.side_effect = ValueError("Invalid param")


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

    @mock.patch('builtins.open', new=mocked_open1)
    def test_open_01(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        check = item.open()

        self.assertIsNotNone(item.file)
        self.assertTrue(check)
        return

    @mock.patch('builtins.open', new=mocked_open2)
    def test_open_02(self):
        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        check = item.open()

        self.assertIsNone(item.file)
        self.assertFalse(check)
        return

    @mock.patch('builtins.open', new=mocked_open3)
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

    @mock.patch('builtins.open', new=mocked_close1)
    def test_close_01(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        check1 = item.open()
        check2 = item.close()

        self.assertTrue(check1)
        self.assertTrue(check2)
        return

    @mock.patch('builtins.open', new=mocked_write1)
    def test_write_01(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        item.open()

        m = Message(app="TEST", tag="RUN", level="INFORM", content="This is a test!")
        item.write(m)

        # noinspection PyUnresolvedReferences
        write_called = item.file.write.called

        # noinspection PyUnresolvedReferences
        flush_called = item.file.flush.called

        # noinspection PyUnresolvedReferences
        call = item.file.write.call_args_list[0]
        (args, kwargs) = call
        data = str(args[0])

        self.assertTrue(write_called)
        self.assertTrue(flush_called)
        self.assertIn(m.app, data)
        self.assertIn(m.tag, data)
        self.assertIn(m.level, data)
        self.assertIn(m.content, data)
        return

    @mock.patch('builtins.open', new=mocked_write2)
    def test_write_02(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        item.open()

        m = Message(app="TEST", level="INFORM", content="This is a test!")
        item.write(m)

        # noinspection PyUnresolvedReferences
        write_called = item.file.write.called

        # noinspection PyUnresolvedReferences
        flush_called = item.file.flush.called

        # noinspection PyUnresolvedReferences
        call = item.file.write.call_args_list[0]
        (args, kwargs) = call
        data = str(args[0])

        self.assertTrue(write_called)
        self.assertTrue(flush_called)
        self.assertIn(m.app, data)
        self.assertIn(m.level, data)
        self.assertIn(m.content, data)
        return

    def test_write_03(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        m = Message(app="TEST", tag="RUN", level="INFORM", content="This is a test!")
        self.assertRaises(ValueError, item.write, m)
        return

    @mock.patch('builtins.open', new=mocked_write4)
    def test_write_04(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        item.open()

        item.file.write.side_effect = OSError

        m = Message(app="TEST", tag="RUN", level="INFORM", content="This is a test!")
        item.write(m)

        # noinspection PyUnresolvedReferences
        write_called = item.file.write.called

        # noinspection PyUnresolvedReferences
        flush_called = item.file.flush.called

        # noinspection PyUnresolvedReferences
        call = item.file.write.call_args_list[0]
        (args, kwargs) = call
        data = str(args[0])

        self.assertTrue(write_called)
        self.assertFalse(flush_called)
        self.assertIn(m.app, data)
        self.assertIn(m.level, data)
        self.assertIn(m.content, data)
        return

    @mock.patch('builtins.open', new=mocked_write5)
    def test_write_05(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        item.open()

        m = Message(content="This is a test!", raw=True)
        item.write(m)

        # noinspection PyUnresolvedReferences
        write_called = item.file.write.called

        # noinspection PyUnresolvedReferences
        flush_called = item.file.flush.called

        # noinspection PyUnresolvedReferences
        call = item.file.write.call_args_list[0]
        (args, kwargs) = call
        data = args[0].decode("utf-8")

        self.assertTrue(write_called)
        self.assertTrue(flush_called)
        self.assertEqual(m.content, data)
        return

    @mock.patch('builtins.open', new=mocked_write6)
    def test_write_06(self):

        item = FileWriter()
        item.setup(text_space=20, filename="tests.log", append_data=True)

        item.open()
        item.file.write.side_effect = OSError

        m = Message(content="This is a test!", raw=True)
        item.write(m)

        # noinspection PyUnresolvedReferences
        write_called = item.file.write.called

        # noinspection PyUnresolvedReferences
        flush_called = item.file.flush.called

        # noinspection PyUnresolvedReferences
        call = item.file.write.call_args_list[0]
        (args, kwargs) = call
        data = args[0].decode("utf-8")

        self.assertTrue(write_called)
        self.assertFalse(flush_called)
        self.assertEqual(m.content, data)
        return

    @mock.patch('builtins.open', new=mocked_write7)
    def test_write_07(self):

        item = FileWriter()
        item.setup(text_space=20)

        m = Message(content="This is a test!", raw=True)

        self.assertRaises(ValueError, item.write, m)
        return
