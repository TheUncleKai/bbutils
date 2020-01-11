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
import unittest
import sys

from typing import List

import bbutil.logging

from bbutil.logging.types import Message, Writer

_default_index = ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]


class TestWriter(Writer):

    def __init__(self, index: list):
        Writer.__init__(self, "TEST", index)
        self.text_space: int = 15
        self.seperator: str = "|"
        self.lines: List[str] = []
        self.fail_open = False
        self.fail_close = False
        self.buffer: List[Message] = []
        return

    def setup(self, **kwargs):
        item = kwargs.get("text_space", None)
        if item is not None:
            self.text_space = item

        item = kwargs.get("seperator", None)
        if item is not None:
            self.seperator = item
        return

    def open(self) -> bool:
        if self.fail_open is True:
            print("{0:s}: Openening failed!".format(self.id))
            return False

        return True

    def close(self) -> bool:
        if self.fail_close is True:
            print("{0:s}: Closing failed!".format(self.id))
            return False
        return True

    def clear(self) -> bool:
        print("CLEAR")
        return True

    def write(self, item: Message):
        self.buffer.append(item)

        if item.raw is True:
            sys.stdout.write(item.content)
            return

        if item.tag == "":
            line = "{0:s} {1:s}: {2:s}".format(item.app, item.level, item.content)
            self.lines.append(line)
            print(line)
        else:
            line = "{0:s} {1:s} {2:s}: {3:s}".format(item.app, item.level, item.tag, item.content)
            self.lines.append(line)
            print(line)
        return


class TestLogging(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_constructor(self):
        log = bbutil.logging.Logging()

        self.assertIsNotNone(log)
        self.assertEqual(log._level, 0)
        self.assertEqual(log._app, "")
        self.assertEqual(log._timer_counter, 0)
        self.assertEqual(log._interval, 0.01)
        self.assertEqual(log.state.open, False)
        self.assertEqual(log.state.close, False)
        self.assertEqual(log.state.use_thread, False)
        self.assertEqual(log.state.thread_active, False)

        self.assertEqual(len(log._timer_list), 0)
        self.assertEqual(len(log._buffer), 0)
        self.assertEqual(len(log._index), 0)
        self.assertEqual(len(log._writer), 0)
        return

    def test_setup(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()

        log.setup(app="TEST", interval=0.02, level=1, index=_index, use_thread=True)

        self.assertEqual(log._level, 1)
        self.assertEqual(log._app, "TEST")
        self.assertEqual(log._timer_counter, 0)
        self.assertEqual(log._interval, 0.02)

        self.assertEqual(log.state.open, False)
        self.assertEqual(log.state.close, False)
        self.assertEqual(log.state.use_thread, True)
        self.assertEqual(log.state.thread_active, False)

        self.assertEqual(len(log._timer_list), 0)
        self.assertEqual(len(log._buffer), 0)
        self.assertEqual(len(log._index), 2)
        self.assertEqual(log._index, _index)
        self.assertEqual(len(log._writer), 0)
        return

    def test_register(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index)
        log.register(writer)

        self.assertIsNotNone(writer)
        self.assertEqual(len(log._writer), 1)
        self.assertIs(log._writer[0], writer)
        return

    def test_open_01(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index)
        log.register(writer)

        check = log.open()
        self.assertTrue(check)

        log.close()
        return

    def test_open_02(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        log.setup(app="TEST", level=1, index=_index)

        check = log.open()

        self.assertFalse(check)

        log.close()
        return

    def test_open_03(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)
        writer.fail_open = True

        log.setup(app="TEST", level=1, index=_index)
        log.register(writer)

        check = log.open()

        self.assertFalse(check)

        log.close()
        return

    def test_open_04(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        check = log.open()

        self.assertTrue(check)

        log.close()
        return

    def test_open_05(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        check1 = log.open()
        check2 = log.open()

        self.assertTrue(check1)
        self.assertFalse(check2)

        log.close()
        return

    def test_close_01(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index)
        log.register(writer)

        check1 = log.open()
        self.assertTrue(check1)

        check2 = log.close()
        self.assertTrue(check2)
        return

    def test_close_02(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)
        writer.fail_close = True

        log.setup(app="TEST", level=1, index=_index)
        log.register(writer)

        check1 = log.open()
        self.assertTrue(check1)

        check2 = log.close()
        self.assertFalse(check2)
        return

    def test_close_03(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        check1 = log.open()
        self.assertTrue(check1)
        self.assertTrue(log.state.thread_active)

        check2 = log.close()
        self.assertTrue(check2)
        self.assertFalse(log.state.thread_active)
        return

    def test_output_01(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=False)
        log.register(writer)

        log.open()

        log.inform("TEST1", "BLA")

        test_string = "TEST INFORM TEST1: BLA"
        self.assertEqual(len(writer.lines), 1)
        self.assertEqual(writer.lines[0], test_string)
        log.close()
        return

    def test_output_02(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=False)
        log.register(writer)

        log.open()

        log.inform("TEST1", "BLA")

        self.assertEqual(len(writer.lines), 0)
        log.close()
        return

    def test_output_03(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=2, index=_index, use_thread=False)
        log.register(writer)

        log.open()

        log.inform("TEST1", "BLA")

        self.assertEqual(len(writer.lines), 0)
        log.close()
        return

    def test_output_04(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(["DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"])

        log.setup(app="TEST", level=1, index=_index, use_thread=False)
        log.register(writer)

        log.open()

        log.inform("TEST1", "BLA")
        self.assertEqual(len(writer.lines), 0)
        log.close()
        return

    def test_output_05(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        log.inform("TEST1", "BLA")

        time.sleep(0.1)

        test_string = "TEST INFORM TEST1: BLA"
        self.assertEqual(len(writer.lines), 1)
        self.assertEqual(writer.lines[0], test_string)
        log.close()
        return

    def test_inform(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        log.inform("TEST1", "BLA")
        time.sleep(0.1)
        log.close()

        item = writer.buffer[0]

        self.assertEqual(item.app, "TEST")
        self.assertEqual(item.level, "INFORM")
        self.assertEqual(item.tag, "TEST1")
        self.assertEqual(item.content, "BLA")
        return

    def test_warn(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        log.warn("TEST1", "BLA")
        time.sleep(0.1)
        log.close()

        item = writer.buffer[0]

        self.assertEqual(item.app, "TEST")
        self.assertEqual(item.level, "WARN")
        self.assertEqual(item.tag, "TEST1")
        self.assertEqual(item.content, "BLA")
        return

    def test_debug1(self):

        _index = {
            0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
            1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        log.debug1("TEST1", "BLA")
        time.sleep(0.1)
        log.close()

        item = writer.buffer[0]

        self.assertEqual(item.app, "TEST")
        self.assertEqual(item.level, "DEBUG1")
        self.assertEqual(item.tag, "TEST1")
        self.assertEqual(item.content, "BLA")
        return

    def test_debug2(self):

        _index = {
            2: ["DEBUG2"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=2, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        log.debug2("TEST1", "BLA")
        time.sleep(0.1)
        log.close()

        item = writer.buffer[0]

        self.assertEqual(item.app, "TEST")
        self.assertEqual(item.level, "DEBUG2")
        self.assertEqual(item.tag, "TEST1")
        self.assertEqual(item.content, "BLA")
        return

    def test_debug3(self):

        _index = {
            3: ["DEBUG3"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=3, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        log.debug3("TEST1", "BLA")
        time.sleep(0.1)
        log.close()

        item = writer.buffer[0]

        self.assertEqual(item.app, "TEST")
        self.assertEqual(item.level, "DEBUG3")
        self.assertEqual(item.tag, "TEST1")
        self.assertEqual(item.content, "BLA")
        return

    def test_error(self):

        _index = {
            0: ["ERROR"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=0, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        log.error("BLA")
        time.sleep(0.1)
        log.close()

        item = writer.buffer[0]

        self.assertEqual(item.app, "TEST")
        self.assertEqual(item.level, "ERROR")
        self.assertEqual(item.tag, "")
        self.assertEqual(item.content, "BLA")
        return

    def test_exception(self):

        _index = {
            0: ["EXCEPTION"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=0, index=_index, use_thread=True)
        log.register(writer)

        log.open()

        e = OSError(2, 'No such file or directory', 'foo')

        log.exception(e)
        time.sleep(0.1)
        log.close()

        self.assertEqual(len(writer.buffer), 2)

        item1 = writer.buffer[0]
        item2 = writer.buffer[1]

        self.assertEqual(item1.app, "TEST")
        self.assertEqual(item1.level, "EXCEPTION")
        self.assertEqual(item1.tag, "")
        self.assertEqual(item1.content, "An exception of type FileNotFoundError occurred.")

        self.assertEqual(item2.app, "TEST")
        self.assertEqual(item2.level, "EXCEPTION")
        self.assertEqual(item2.tag, "")
        return

    def test_traceback(self):

        _index = {
            0: ["EXCEPTION", "ERROR"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=0, index=_index, use_thread=False)
        log.register(writer)

        log.open()

        try:
            _ = 10 / 0
        except ZeroDivisionError:
            log.traceback()

        log.close()

        length = len(writer.buffer)
        self.assertEqual(length, 4)
        self.assertEqual(writer.buffer[0].content, "Uncaught exception")
        self.assertEqual(writer.buffer[1].content, "Type:  <class 'ZeroDivisionError'>")
        self.assertEqual(writer.buffer[2].content, "Value: division by zero")
        return

    def test_progress(self):

        _index = {
            0: ["PROGRESS"],
        }

        log = bbutil.logging.Logging()

        log.setup(app="TEST", level=0, index=_index, use_thread=False)

        progress = log.progress(100)
        self.assertIsNotNone(progress)
        return

    def test_timer(self):

        _index = {
            0: ["PROGRESS"],
        }

        log = bbutil.logging.Logging()

        log.setup(app="TEST", level=0, index=_index, use_thread=False)

        timer = log.timer("Time to stop")
        self.assertIsNotNone(timer)
        return

    def test_raw(self):

        _index = {
            0: ["EXCEPTION", "ERROR"],
        }

        log = bbutil.logging.Logging()
        writer = TestWriter(_default_index)

        log.setup(app="TEST", level=0, index=_index, use_thread=False)
        log.register(writer)

        log.open()

        log.raw("this is pure")

        log.close()

        length = len(writer.buffer)
        self.assertEqual(length, 1)
        self.assertEqual(writer.buffer[0].content, "this is pure")
        return

    def test_get_writer_01(self):

        log = bbutil.logging.Logging()
        item = log.get_writer("console")

        self.assertIsNotNone(item)
        return

    def test_get_writer_02(self):

        log = bbutil.logging.Logging()
        self.assertRaises(ImportError, log.get_writer, "xconsole")
        return
