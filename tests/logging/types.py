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
from bbutil.logging.types import Message, Progress, Timer


class Callback(object):

    def __init__(self):
        self.item = None
        return

    def append(self, item: Message):
        self.item = item
        return


class TestMessage(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_constructor_01(self):
        message = Message()

        self.assertIsNotNone(message)
        self.assertIsNotNone(message.time)
        self.assertEqual(message.app, "")
        self.assertEqual(message.tag, "")
        self.assertEqual(message.content, "")
        self.assertEqual(message.level, "")
        self.assertEqual(message.raw, False)
        self.assertIsNone(message.progress)
        return

    def test_constructor_02(self):
        progress = Progress(100, 0, None)
        message = Message(app="TOSS", tag="TAGIT", content="LILO", level="HUH", raw=True, progress=progress)

        self.assertIsNotNone(message)
        self.assertIsNotNone(message.time)
        self.assertEqual(message.app, "TOSS")
        self.assertEqual(message.tag, "TAGIT")
        self.assertEqual(message.content, "LILO")
        self.assertEqual(message.level, "HUH")
        self.assertEqual(message.raw, True)
        self.assertIsNotNone(message.progress)
        self.assertEqual(message.progress, progress)
        return


class TestTimer(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_constructor(self):
        callback = Callback()

        item = Timer("Message", callback.append)

        self.assertIsNotNone(item)
        self.assertEqual(item.content, "Message")
        self.assertIsNotNone(item._append)
        return

    def test_stop(self):
        callback = Callback()

        item = Timer("Message", callback.append)
        time.sleep(0.1)

        item.stop()

        print(callback.item.content)

        self.assertIsNotNone(callback.item)
        self.assertNotEqual(callback.item.content, "")
        self.assertEqual(callback.item.level, "TIMER")
        return


class TestProgress(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_constructor(self):
        callback = Callback()

        item = Progress(100, 10, callback.append)

        self.assertIsNotNone(item)
        self.assertEqual(item.limit, 100)
        self.assertEqual(item.counter, 0)
        self.assertEqual(item.finished, False)
        self.assertEqual(item.interval, 10)
        self.assertEqual(item.interval_counter, 0)
        self.assertIsNotNone(item.append)
        return

    def test_inc_01(self):
        callback = Callback()

        item = Progress(100, 0, callback.append)
        item.inc()

        message = callback.item

        self.assertIsNotNone(message)
        self.assertIs(message.progress, item)
        self.assertEqual(message.level, "PROGRESS")
        return

    def test_inc_02(self):
        callback = Callback()

        item = Progress(100, 2, callback.append)

        item.inc()
        message1 = callback.item

        item.inc()
        message2 = callback.item

        self.assertIsNotNone(callback.item)

        self.assertIsNone(message1)

        self.assertIsNotNone(message2)
        self.assertIs(message2.progress, item)
        self.assertEqual(message2.level, "PROGRESS")
        return

    def test_inc_03(self):
        callback = Callback()

        item = Progress(100, 0, callback.append)
        item.counter = 99
        item.inc()

        message = callback.item

        self.assertIsNotNone(message)
        self.assertIs(message.progress, item)
        self.assertEqual(message.level, "PROGRESS")
        self.assertTrue(item.finished)
        return

    def test_dec_01(self):
        callback = Callback()

        item = Progress(100, 0, callback.append)
        item.counter = 1
        item.dec()

        message = callback.item

        self.assertIsNotNone(message)
        self.assertIs(message.progress, item)
        self.assertEqual(message.level, "PROGRESS")
        self.assertEqual(item.counter, 0)
        return

    def test_dec_02(self):
        callback = Callback()

        item = Progress(100, 10, callback.append)
        item.counter = 1
        item.dec()

        message = callback.item

        self.assertIsNone(message)
        self.assertEqual(item.counter, 0)
        return
