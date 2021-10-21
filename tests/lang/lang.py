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

import os.path
import unittest

from bbutil.lang import Lang
from bbutil.utils import full_path


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

    # noinspection PyUnresolvedReferences
    def test_setup_01(self):
        lang = Lang()

        _check = lang.setup(localedir="")

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check, False, "_check != False")
        self.assertEqual(lang.is_setup, False, "is_setup != False")
        return

    # noinspection PyUnresolvedReferences
    def test_setup_02(self):
        lang = Lang()

        _locales = full_path("tests/locales")

        _check = lang.setup(localedir=_locales)

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check, True, "_check != True")
        self.assertEqual(lang.is_setup, True, "is_setup != True")
        self.assertEqual(lang.localedir, _locales, "localedir != {0:s}".format(_locales))
        self.assertEqual(lang.used_lang, "en", "used_lang != en")
        self.assertEqual(lang.use_dummy, False, "use_dummy != False")
        return

    # noinspection PyUnresolvedReferences
    def test_setup_03(self):
        lang = Lang()

        _locales = full_path("tests/locales")

        _check = lang.setup(localedir=_locales, used_lang="de")

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check, True, "_check != True")
        self.assertEqual(lang.is_setup, True, "is_setup != True")
        self.assertEqual(lang.localedir, _locales, "localedir != {0:s}".format(_locales))
        self.assertEqual(lang.used_lang, "de", "used_lang != de")
        self.assertEqual(lang.use_dummy, False, "use_dummy != False")
        return

    # noinspection PyUnresolvedReferences
    def test_setup_04(self):
        lang = Lang()

        _locales = full_path("tests-www/locales")

        _check = lang.setup(localedir=_locales, used_lang="de")

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check, False, "_check != False")
        self.assertEqual(lang.is_setup, False, "is_setup != False")
        self.assertEqual(lang.use_dummy, True, "use_dummy != True")
        return

    # noinspection PyUnresolvedReferences
    def test_setup_05(self):
        os.environ["IGNORE_GETTEXT"] = "1"
        lang = Lang()

        _locales = full_path("tests/locales")

        _check = lang.setup(localedir=_locales, used_lang="de")

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check, True, "_check != True")
        self.assertEqual(lang.is_setup, True, "is_setup != True")
        self.assertEqual(lang.localedir, _locales, "localedir != {0:s}".format(_locales))
        self.assertEqual(lang.used_lang, "de", "used_lang != de")
        self.assertEqual(lang.use_dummy, True, "use_dummy != True")

        os.environ.pop('IGNORE_GETTEXT')
        return

    # noinspection PyUnresolvedReferences
    def test_dummy_01(self):
        lang = Lang()

        _test = "test1"

        _value = lang.dummy(_test)

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_value, _test, "_value != _test")
        return
