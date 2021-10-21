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

from bbutil.lang import Lang, Domain
from bbutil.utils import full_path


def _set_dummy(language):
    return language


_ = _set_dummy


def set_lang(hook_func):
    global _
    _ = hook_func
    return


class _TestHook(object):

    def __init__(self):
        self.hook_number: int = 0
        return

    # noinspection PyUnusedLocal
    def set_hook(self, language):
        self.hook_number += 1
        return


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

    # noinspection PyUnresolvedReferences
    def test_add_01(self):
        os.environ["IGNORE_GETTEXT"] = "1"
        lang = Lang()

        _check1 = lang.setup("tests/locales")

        lang.add("test", _set_dummy)

        _length = len(lang.domains)

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_length, 1, "_length != 1")

        os.environ.pop('IGNORE_GETTEXT')
        return

    # noinspection PyUnresolvedReferences
    def test_add_02(self):
        os.environ["IGNORE_GETTEXT"] = "1"
        lang = Lang()

        _check1 = lang.setup("tests/locales")

        lang.add("test", _set_dummy)
        _length1 = len(lang.domains)

        lang.add("test", _set_dummy)
        _length2 = len(lang.domains)

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_length1, 1, "_length1 != 1")
        self.assertEqual(_length2, 1, "_length1 != 1")

        os.environ.pop('IGNORE_GETTEXT')
        return

    # noinspection PyUnresolvedReferences
    def test_set_language_01(self):
        os.environ["IGNORE_GETTEXT"] = "1"
        lang = Lang()

        _hook = _TestHook()

        _check1 = lang.setup("tests/locales")

        lang.add("test", _hook.set_hook)
        _num1 = _hook.hook_number

        lang.set_language("de")
        _num2 = _hook.hook_number

        self.assertNotEqual(lang, None, "Lang: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_num1, 1, "_num1 != 1")
        self.assertEqual(_num2, 2, "_num2 != 2")

        os.environ.pop('IGNORE_GETTEXT')
        return


class TestDomain(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        return

    def tearDown(self):
        return

    # noinspection PyUnresolvedReferences
    def test_constructor_01(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=True, ignore=None, used_lang="de")

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertEqual(_domain.domain, "test", "domain != test")
        self.assertEqual(_domain.gettext, None, "gettext != None")
        self.assertEqual(_domain.lang, None, "lang != None")
        self.assertEqual(_domain.is_set, False, "is_set != False")
        self.assertEqual(_domain.ignore, None, "ignore != None")
        self.assertEqual(len(_domain.callback), 0, "len != 0")
        self.assertEqual(_domain.used_lang, "de", "used_lang != de")
        self.assertEqual(_domain.use_dummy, True, "use_dummy != True")
        return

    # noinspection PyUnresolvedReferences
    def test_create_01(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=True, ignore=None, used_lang="de")

        _domain.create()

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertNotEqual(_domain.lang, None, "lang == None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        return

    # noinspection PyUnresolvedReferences
    def test_create_02(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=True, ignore=None, used_lang="de")
        _domain.is_set = True

        _domain.create()

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertEqual(_domain.lang, None, "lang != None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        return

    # noinspection PyUnresolvedReferences
    def test_create_03(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=False, ignore=1, used_lang="de")

        _domain.create()

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertNotEqual(_domain.lang, None, "lang == None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        return

    # noinspection PyUnresolvedReferences
    def test_create_04(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=False, ignore=None, used_lang="de")
        _domain.create()

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertNotEqual(_domain.lang, None, "lang == None")
        self.assertNotEqual(_domain.gettext, None, "gettext == None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        return

    # noinspection PyUnresolvedReferences
    def test_load_01(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=False, ignore=None, used_lang="de")

        _domain.callback.append(set_lang)

        _domain.create()
        _domain.load()

        _test1 = _("Test1")

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertNotEqual(_domain.lang, None, "lang == None")
        self.assertNotEqual(_domain.gettext, None, "gettext == None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        self.assertEqual(_test1, "Test_DE", "_test1 != Test_DE")
        return

    # noinspection PyUnresolvedReferences
    def test_load_02(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=False, ignore=None, used_lang="en")

        _domain.callback.append(set_lang)

        _domain.create()
        _domain.load()

        _test1 = _("Test1")

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertNotEqual(_domain.lang, None, "lang == None")
        self.assertNotEqual(_domain.gettext, None, "gettext == None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        self.assertEqual(_test1, "Test_EN", "_test1 != Test_DE")
        return

    # noinspection PyUnresolvedReferences
    def test_load_03(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=False, ignore=None, used_lang="en")
        _domain.callback.append(set_lang)

        _domain.is_set = False
        _domain.used_lang = "en"
        _domain.create()
        _domain.load()
        _test1 = _("Test1")

        _domain.is_set = False
        _domain.used_lang = "de"
        _domain.create()
        _domain.load()
        _test2 = _("Test1")

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertNotEqual(_domain.lang, None, "lang == None")
        self.assertNotEqual(_domain.gettext, None, "gettext == None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        self.assertEqual(_test1, "Test_EN", "_test1 != Test_DE")
        self.assertEqual(_test2, "Test_DE", "_test1 != Test_DE")
        return

    # noinspection PyUnresolvedReferences
    def test_load_04(self):
        _locales = full_path("tests/locales")

        _domain = Domain(localedir=_locales, domain="test", use_dummy=True, ignore=None, used_lang="en")
        _domain.callback.append(set_lang)

        _domain.create()
        _domain.load()
        _test1 = _("Test1")

        self.assertNotEqual(_domain, None, "_domain: None")
        self.assertEqual(_domain.localedir, _locales, "localedir != None")
        self.assertNotEqual(_domain.lang, None, "lang == None")
        self.assertEqual(_domain.gettext, None, "gettext != None")
        self.assertEqual(_domain.is_set, True, "is_set != False")
        self.assertEqual(_test1, "Test1", "_test1 != Test1")
        return
