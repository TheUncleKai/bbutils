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

import bbutil.lang.parser.pyfile

from bbutil.lang.parser.pyfile import PythonFile

from bbutil.utils import full_path

from bbutil.logging import Logging

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}


class TestPythonFile(unittest.TestCase):
    """Testing class for locking module."""

    @staticmethod
    def set_log() -> Logging:
        log = Logging()
        log.setup(app="Test", level=3, index=_index)

        console = log.get_writer("console")
        log.register(console)
        log.open()
        return log

    def setUp(self):
        _log = self.set_log()

        bbutil.lang.parser.pyfile.set_log(_log)
        return

    def tearDown(self):
        return

    # noinspection PyUnresolvedReferences
    def test_constructor_01(self):
        _root = full_path("{0:s}/testlang".format(os.getcwd()))
        _filename = full_path("{0:s}/test1/__init__.py".format(_root))
        _module = "testlang"

        _pyfile = PythonFile(root_path=_root, filename=_filename, module=_module)

        self.assertNotEqual(_pyfile, None, "_pyfile: None")
        return

    def test_create_01(self):
        _root = full_path("{0:s}/testlang".format(os.getcwd()))
        _filename = full_path("{0:s}/test1/__init__.py".format(_root))
        _locales = full_path("{0:s}/.locales".format(_root))
        _module = "testlang"

        _pyfile = PythonFile(root_path=_root,
                             filename=_filename,
                             module=_module,
                             module_filter="testlang.test1",
                             locales=_locales)
        _check1 = _pyfile.create()

        self.assertNotEqual(_pyfile, None, "_pyfile: None")
        self.assertEqual(_check1, True, "_check != True")
        self.assertEqual(_pyfile.path, '/home/raphahk/projekte/bbutils/testlang/.locales/gui')
        self.assertEqual(_pyfile.pot, '/home/raphahk/projekte/bbutils/testlang/.locales/gui/_testlang.test1.pot')
        self.assertEqual(_pyfile.domain, 'gui')
        self.assertEqual(_pyfile.classname, 'testlang.test1')
        return

    def test_create_02(self):
        _root = full_path("{0:s}/testlang".format(os.getcwd()))
        _filename = full_path("{0:s}/test1/__init__.py".format(_root))
        _locales = full_path("{0:s}/.locales".format(_root))
        _module = "testlang"

        _pyfile = PythonFile(root_path=_root,
                             filename=_filename,
                             module=_module,
                             module_filter="testlang.test2",
                             locales=_locales)
        _check1 = _pyfile.create()

        self.assertNotEqual(_pyfile, None, "_pyfile: None")
        self.assertEqual(_check1, False, "_check != False")
        return

    def test_create_03(self):
        _root = full_path("{0:s}/testlang".format(os.getcwd()))
        _filename = full_path("{0:s}/test2/__init__.py".format(_root))
        _locales = full_path("{0:s}/.locales".format(_root))
        _module = "testlang"

        _pyfile = PythonFile(root_path=_root,
                             filename=_filename,
                             module=_module,
                             module_filter="testlang.test2",
                             locales=_locales)
        _check1 = _pyfile.create()

        self.assertNotEqual(_pyfile, None, "_pyfile: None")
        self.assertEqual(_check1, False, "_check != False")
        return
