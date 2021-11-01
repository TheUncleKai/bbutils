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
