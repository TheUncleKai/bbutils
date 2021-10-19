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

from bbutil.lang import Lang


class TestLang(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        return

    def tearDown(self):
        return

    # noinspection PyUnresolvedReferences
    def test_constructor_01(self):
        lang = Lang()

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(lang.localedir, None, "localedir != None")
        self.assertEqual(lang.do_setup, False, "do_setup != False")
        self.assertEqual(lang.used_lang, None, "used_lang != None")
        self.assertEqual(lang.use_dummy, False, "use_dummy != False")
        self.assertEqual(lang.is_setup, False, "is_setup != False")
        return
