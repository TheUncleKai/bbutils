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
