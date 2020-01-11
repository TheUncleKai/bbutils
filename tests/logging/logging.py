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
from typing import List

import bbutil.logging
import bbutil.types

from bbutil.types import Message, Writer


class TestWriter(Writer):

    def __init__(self):
        _index = ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
        Writer.__init__(self, "TEST", _index)

        self.text_space: int = 15
        self.seperator: str = "|"
        self.lines: List[str] = []
        self.fail_open = False
        self.fail_close = False
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
        writer = TestWriter()

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
        writer = TestWriter()

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
        writer = TestWriter()
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
        writer = TestWriter()

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
        writer = TestWriter()

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
        writer = TestWriter()

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
        writer = TestWriter()
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
        writer = TestWriter()

        log.setup(app="TEST", level=1, index=_index, use_thread=True)
        log.register(writer)

        check1 = log.open()
        self.assertTrue(check1)
        self.assertTrue(log.state.thread_active)

        check2 = log.close()
        self.assertTrue(check2)
        self.assertFalse(log.state.thread_active)
        return
