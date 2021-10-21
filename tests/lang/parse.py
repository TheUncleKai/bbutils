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
import os
import unittest

import bbutil.lang.parser

from bbutil.lang.parser import Parser
from bbutil.utils import full_path

from bbutil.logging import Logging


class TestParser(unittest.TestCase):
    """Testing class for locking module."""

    @staticmethod
    def set_log() -> Logging:
        log = Logging()
        log.setup(app="Test")

        console = log.get_writer("console")
        log.register(console)
        log.open()
        return log

    def setUp(self):
        bbutil.lang.parser.set_log(self.set_log())
        return

    def tearDown(self):
        return

    # noinspection PyUnresolvedReferences
    def test_constructor_01(self):
        _parser = Parser()

        self.assertNotEqual(_parser, None, "_parser: None")
        return

    # noinspection PyUnresolvedReferences
    def test_setup_01(self):
        _parser = Parser()

        _check = _parser.setup()

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check, False, "_check != False")
        return

    # noinspection PyUnresolvedReferences
    def test_setup_02(self):
        _locales = full_path("tests/locales")

        _parser = Parser()

        _check = _parser.setup(locales=_locales, module="tests.example")

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check, True, "_check != True")
        return

    # noinspection PyUnresolvedReferences
    def test_parse_01(self):
        _locales = full_path("tests/locales")
        _root = os.getcwd()

        _parser = Parser()

        _check1 = _parser.setup(locales=_locales, module="testlang", root=_root)

        _check2 = _parser.parse()

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check != True")
        self.assertEqual(_check2, True, "_check != True")
        return
