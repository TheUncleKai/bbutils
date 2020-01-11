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
import unittest
import unittest.mock as mock

from bbutil.logging.writer.console import ConsoleWriter
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

        item = ConsoleWriter()

        self.assertEqual(len(item.styles), 8)
        self.assertEqual(len(item.error_index), 0)
        self.assertEqual(item.encoding, "")
        self.assertEqual(item.text_space, 15)
        self.assertEqual(item.seperator, "|")
        self.assertEqual(item.length, 0)
        self.assertEqual(item.bar_len, 50)
        self.assertIs(item.stdout, sys.stdout)
        self.assertIs(item.stderr, sys.stderr)
        self.assertFalse(item.use_error)
        return

    def test_setup(self):

        item = ConsoleWriter()
        item.setup(text_space=20, seperator="#", error_index=["INFORM"], bar_len=40)

        self.assertEqual(len(item.styles), 8)
        self.assertEqual(len(item.error_index), 1)
        self.assertEqual(item.encoding, "")
        self.assertEqual(item.text_space, 20)
        self.assertEqual(item.seperator, "#")
        self.assertEqual(item.length, 0)
        self.assertEqual(item.bar_len, 40)
        self.assertIs(item.stdout, sys.stdout)
        self.assertIs(item.stderr, sys.stderr)
        self.assertFalse(item.use_error)
        return

    def test_add_style(self):

        item = ConsoleWriter()
        item.add_style("XXX", "BRIGHT", "GREEN", "")
        self.assertEqual(len(item.styles), 9)
        self.assertEqual(item.styles["XXX"].name, "XXX")
        return

    def test_open(self):

        item = ConsoleWriter()
        item.open()

        self.assertNotEqual(item.encoding, "")
        return

    def test_write_01(self):

        message = Message(app="TEST", level="INFORM", tag="TEST", content="This is a test!")

        item = ConsoleWriter()
        item.open()
        item.stdout = SysWrite()

        item.write(message)

        write_called = item.stdout.write.called
        call = item.stdout.write.call_args_list[0]
        (args, kwargs) = call
        data = args[0]

        print(data)

        self.assertTrue(write_called)
        self.assertIn(message.app, data)
        self.assertIn(message.tag, data)
        self.assertIn(message.content, data)
        return

    def test_write_02(self):

        message = Message(app="TEST", content="This is a test!", raw=True)

        item = ConsoleWriter()
        item.open()
        item.stdout = SysWrite()

        item.write(message)

        write_called = item.stdout.write.called
        call = item.stdout.write.call_args_list[0]
        (args, kwargs) = call
        data = args[0]

        self.assertTrue(write_called)
        self.assertNotIn(message.app, data)
        self.assertIn(message.content, data)
        return

    def test_write_03(self):

        message = Message(app="TEST", level="INFORM", content="This is a test!")

        item = ConsoleWriter()
        item.open()
        item.stdout = SysWrite()

        item.write(message)

        write_called = item.stdout.write.called
        call = item.stdout.write.call_args_list[0]
        (args, kwargs) = call
        data = args[0]

        self.assertTrue(write_called)
        self.assertIn(message.app, data)
        self.assertIn(message.content, data)
        return

    def test_write_04(self):

        message = Message(app="TEST", level="ERROR", content="This is a test!")

        item = ConsoleWriter()
        item.setup(error_index=["ERROR"])
        item.open()
        item.stderr = SysWrite()

        item.write(message)

        write_called = item.stderr.write.called
        call = item.stderr.write.call_args_list[0]
        (args, kwargs) = call
        data = args[0]

        print(data)

        self.assertTrue(write_called)
        self.assertIn(message.app, data)
        self.assertIn(message.content, data)
        return

    def test_write_05(self):

        writer = ConsoleWriter()
        writer.open()
        writer.stdout = SysWrite()

        callback = Callback(writer)

        progress = Progress(100, 0, callback.append)

        n = 0
        while True:
            progress.inc()
            time.sleep(0.0001)
            n += 1
            if progress.finished is True:
                break

        write_called = writer.stdout.write.called
        count = writer.stdout.write.call_count
        self.assertEqual(n, 100)
        self.assertEqual(count, 101)
        self.assertTrue(write_called)
        return

    def test_write_06(self):

        writer = ConsoleWriter()
        writer.open()
        writer.stdout = SysWrite()

        callback = Callback(writer)

        progress = Progress(100, 0, callback.append)
        writer.line_width = 20

        n = 0
        while True:
            progress.inc()
            time.sleep(0.0001)
            n += 1
            if progress.finished is True:
                break

        write_called = writer.stdout.write.called
        count = writer.stdout.write.call_count

        self.assertEqual(n, 100)
        self.assertEqual(count, 0)
        self.assertFalse(write_called)
        return

    def test_clear_01(self):

        message = Message(app="TEST", content="This is a test!", raw=True)

        item = ConsoleWriter()
        item.open()
        item.stdout = SysWrite()

        item.write(message)
        item.clear()

        count = item.stdout.write.call_count
        write_called = item.stdout.write.called
        call = item.stdout.write.call_args_list[1]
        (args, kwargs) = call
        data = args[0]

        self.assertTrue(write_called)
        self.assertIn('\r', data)
        self.assertEqual(count, 2)
        return

    def test_clear_02(self):

        message = Message(app="TEST", content="This is a test!", level="ERROR")

        item = ConsoleWriter()
        item.setup(error_index=["ERROR"])
        item.open()
        item.stderr = SysWrite()

        item.write(message)
        item.clear()

        count = item.stderr.write.call_count
        write_called = item.stderr.write.called
        call = item.stderr.write.call_args_list[1]
        (args, kwargs) = call
        data = args[0]

        self.assertTrue(write_called)
        self.assertIn('\r', data)
        self.assertEqual(count, 2)
        return
