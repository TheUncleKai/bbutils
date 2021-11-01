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
import sys

import bbutil.lang.parser
import bbutil.lang.parser.pyfile

from bbutil.lang.parser import Parser

from bbutil.utils import full_path

from bbutil.logging import Logging

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}


class TestParser(unittest.TestCase):
    """Testing class for locking module."""

    @staticmethod
    def set_log() -> Logging:
        log = Logging()
        log.setup(app="Test", level=2, index=_index)

        console = log.get_writer("console")
        log.register(console)
        log.open()
        return log

    def setUp(self):
        _log = self.set_log()

        bbutil.lang.parser.set_log(_log)
        bbutil.lang.parser.pyfile.set_log(_log)
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

        _root = full_path("{0:s}/testdata".format(os.getcwd()))
        sys.path.append(_root)

        _package = full_path("{0:s}/testlang".format(_root))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)
        _check2 = _parser.parse()

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check != True")
        self.assertEqual(_parser.file_number, 2, "_parser.file_number != 2")
        self.assertEqual(_check2, True, "_check != True")
        return

    # noinspection PyUnresolvedReferences
    def test_parse_02(self):
        _locales = full_path("tests/locales")

        _root = full_path("{0:s}/testdata".format(os.getcwd()))
        sys.path.append(_root)

        _package = full_path("{0:s}/testlang".format(_root))

        _scripts = [
            full_path("{0:s}/testos1.py".format(_root)),
            full_path("{0:s}/testos2.py".format(_root))
        ]

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                module="testlang",
                                filter="testlang.test1",
                                script=_scripts,
                                package_path=_package)
        _check2 = _parser.parse()

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check != True")
        self.assertEqual(_parser.file_number, 4, "_parser.file_number != 4")
        self.assertEqual(_check2, True, "_check != True")
        return

    # noinspection PyUnresolvedReferences
    def test_parse_03(self):
        _locales = full_path("tests/locales")

        _root = full_path("{0:s}/testdata".format(os.getcwd()))
        sys.path.append(_root)

        _package = full_path("{0:s}/testlang".format(_root))

        _scripts = [
            full_path("{0:s}/testos1.py".format(_root)),
            full_path("{0:s}/testos2.py".format(_root)),
            full_path("{0:s}/testos3.py".format(_root))
        ]

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                module="testlang",
                                filter="testlang.test1",
                                script=_scripts,
                                package_path=_package)
        _check2 = _parser.parse()

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check != True")
        self.assertEqual(_parser.file_number, 4, "_parser.file_number != 4")
        self.assertEqual(_check2, True, "_check != True")
        return

    # noinspection PyUnresolvedReferences
    def test_generate_01(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_testdata)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.generate()

        _file1_out = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file1_in = full_path("{0:s}/testdata/testlang/test1/__init__.py".format(_root))

        _file2_out = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file2_in = full_path("{0:s}/testdata/testlang/test1/tester.py".format(_root))

        _lines = [
            'echo "Create _testlang.test1.pot"',
            'xgettext -L python -d gui -o {0:s} {1:s}'.format(_file1_out, _file1_in),
            'echo "Create _testlang.test1.tester.pot"',
            'xgettext -L python -d gui -o {0:s} {1:s}'.format(_file2_out, _file2_in)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 4, "_parser.length != 4")
        self.assertListEqual(_lines, _parser.script_line)
        return

    # noinspection PyUnresolvedReferences
    def test_generate_02(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_testdata)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                windows=True,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.generate()

        _file1_out = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file1_in = full_path("{0:s}/testdata/testlang/test1/__init__.py".format(_root))

        _file2_out = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file2_in = full_path("{0:s}/testdata/testlang/test1/tester.py".format(_root))

        _lines = [
            'echo Create _testlang.test1.pot',
            'xgettext.exe -L python -d gui -o {0:s} {1:s}'.format(_file1_out, _file1_in),
            'echo Create _testlang.test1.tester.pot',
            'xgettext.exe -L python -d gui -o {0:s} {1:s}'.format(_file2_out, _file2_in)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 4, "_parser.length != 4")
        self.assertListEqual(_lines, _parser.script_line)
        return

    # noinspection PyUnresolvedReferences
    def test_merge_01(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_testdata)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.merge()

        _file1_in = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file2_in = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file_out = full_path("{0:s}/.locales/gui/gui.pot".format(_root))

        _lines = [
            'echo "Merge gui.pot"',
            'msgcat {0:s} {1:s} -o {2:s}'.format(_file1_in, _file2_in, _file_out)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 2, "_parser.length != 2")
        self.assertListEqual(_lines, _parser.script_line)
        return

    # noinspection PyUnresolvedReferences
    def test_merge_02(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_testdata)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                windows=True,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.merge()

        _file1_in = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file2_in = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file_out = full_path("{0:s}/.locales/gui/gui.pot".format(_root))

        _lines = [
            'echo Merge gui.pot',
            'msgcat.exe {0:s} {1:s} -o {2:s}'.format(_file1_in, _file2_in, _file_out)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 2, "_parser.length != 2")
        self.assertListEqual(_lines, _parser.script_line)
        return

    # noinspection PyUnresolvedReferences
    def test_copy_01(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_root)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.copy()

        _pot = full_path("{0:s}/.locales/gui/gui.pot".format(_root))
        _po_en = full_path("{0:s}/tests/locales/en/LC_MESSAGES/gui.po".format(_root))
        _po_de = full_path("{0:s}/tests/locales/de/LC_MESSAGES/gui.po".format(_root))

        _lines = [
            'echo "Update en/gui"',
            'cp {0:s} {1:s}'.format(_pot, _po_en),
            'echo "Update de/gui"',
            'cp {0:s} {1:s}'.format(_pot, _po_de)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 4, "_parser.length != 4")
        self.assertListEqual(_lines, _parser.script_line)
        return

    # noinspection PyUnresolvedReferences
    def test_copy_02(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_root)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                windows=True,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.copy()

        _pot = full_path("{0:s}/.locales/gui/gui.pot".format(_root))
        _po_en = full_path("{0:s}/tests/locales/en/LC_MESSAGES/gui.po".format(_root))
        _po_de = full_path("{0:s}/tests/locales/de/LC_MESSAGES/gui.po".format(_root))

        _lines = [
            'echo Update en/gui',
            'copy {0:s} {1:s}'.format(_pot, _po_en),
            'echo Update de/gui',
            'copy {0:s} {1:s}'.format(_pot, _po_de)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 4, "_parser.length != 4")
        self.assertListEqual(_lines, _parser.script_line)
        return

    # noinspection PyUnresolvedReferences
    def test_update_01(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_root)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.update()

        _pot = full_path("{0:s}/.locales/gui/gui.pot".format(_root))
        _po_en = full_path("{0:s}/tests/locales/en/LC_MESSAGES/gui.po".format(_root))
        _po_de = full_path("{0:s}/tests/locales/de/LC_MESSAGES/gui.po".format(_root))

        _lines = [
            'echo "Update en/gui"',
            'msgmerge -N -U {0:s} {1:s}'.format(_po_en, _pot),
            'echo "Update de/gui"',
            'msgmerge -N -U {0:s} {1:s}'.format(_po_de, _pot),
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 4, "_parser.length != 4")
        self.assertListEqual(_lines, _parser.script_line)
        return

    # noinspection PyUnresolvedReferences
    def test_update_02(self):
        _locales = full_path("tests/locales")

        _root = os.getcwd()
        _testdata = full_path("{0:s}/testdata".format(_root))
        sys.path.append(_root)

        _package = full_path("{0:s}/testlang".format(_testdata))

        _parser = Parser()
        _check1 = _parser.setup(locales=_locales,
                                windows=True,
                                module="testlang",
                                filter="testlang.test1",
                                package_path=_package)

        _check2 = _parser.parse()
        _parser.update()

        _pot = full_path("{0:s}/.locales/gui/gui.pot".format(_root))
        _po_en = full_path("{0:s}/tests/locales/en/LC_MESSAGES/gui.po".format(_root))
        _po_de = full_path("{0:s}/tests/locales/de/LC_MESSAGES/gui.po".format(_root))

        _lines = [
            'echo Update en/gui',
            'msgmerge.exe -N -U {0:s} {1:s}'.format(_po_en, _pot),
            'echo Update de/gui',
            'msgmerge.exe -N -U {0:s} {1:s}'.format(_po_de, _pot),
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_parser.length, 4, "_parser.length != 4")
        self.assertListEqual(_lines, _parser.script_line)
        return
