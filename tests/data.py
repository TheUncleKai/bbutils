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

from bbutil.data import Data

members = [
    "A",
    "B",
    "name",
    "lola"
]

values = [
    0.01,
    10,
    "Lola",
    False
]

values2 = [
    0.01,
    10,
    False
]


class TestData(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        return

    def tearDown(self):
        return

    # noinspection PyUnresolvedReferences
    def test_constructor_01(self):
        data = Data(id="Config.Test",
                    keys=members,
                    values=values)

        self.assertNotEqual(data, None, "BaseData: None")
        self.assertEqual(data.A, 0.01, "config.A: 0.01")
        self.assertEqual(data.B, 10, "config.B: 10")
        self.assertEqual(data.name, "Lola", "config.name: Lola")
        self.assertEqual(data.lola, False, "config.lola: False")
        self.assertEqual(str(data), "Config.Test", "data: Config.Test")
        return

    def test_constructor_02(self):
        data = Data(id="Config.Test",
                    values=values2)

        self.assertNotEqual(data, None, "BaseData: None")
        return

    def test_constructor_03(self):
        data = Data(id="Config.Test",
                    keys=members,
                    values=values2)

        self.assertNotEqual(data, None, "BaseData: None")
        return
