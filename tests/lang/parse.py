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
import unittest.mock as mock
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


mock_store_generate_01 = unittest.mock.mock_open()
mock_store_generate_02 = unittest.mock.mock_open()
mock_store_generate_03 = unittest.mock.mock_open()
mock_store_update_01 = unittest.mock.mock_open()
mock_store_update_02 = unittest.mock.mock_open()
mock_store_copy_01 = unittest.mock.mock_open()
mock_store_copy_02 = unittest.mock.mock_open()
mock_store_compile_01 = unittest.mock.mock_open()
mock_store_compile_02 = unittest.mock.mock_open()

mock_store_generate_03.side_effect = OSError(5)
mock_store_update_02.side_effect = OSError(5)
mock_store_copy_02.side_effect = OSError(5)
mock_store_compile_02.side_effect = OSError(5)


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

    @staticmethod
    def _create_test_list(command: str, is_windows: bool = False, newline: bool = False) -> list:
        _root = os.getcwd()

        _ext = ""
        _echo = '"'
        _newline = ""
        _copy = "cp"

        if is_windows is True:
            _ext = ".exe"
            _echo = ""
            _copy = "copy"

        if newline is True:
            _newline = "\n"

        _file1_pot = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file1_py = full_path("{0:s}/testdata/testlang/test1/__init__.py".format(_root))

        _file2_pot = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file2_py = full_path("{0:s}/testdata/testlang/test1/tester.py".format(_root))

        _domain_pot = full_path("{0:s}/.locales/gui/gui.pot".format(_root))

        _po_en = full_path("{0:s}/tests/locales/en/LC_MESSAGES/gui.po".format(_root))
        _po_de = full_path("{0:s}/tests/locales/de/LC_MESSAGES/gui.po".format(_root))

        _mo_en = full_path("{0:s}/tests/locales/en/LC_MESSAGES/gui.mo".format(_root))
        _mo_de = full_path("{0:s}/tests/locales/de/LC_MESSAGES/gui.mo".format(_root))

        _ret = []

        if command == "generate":
            _ret.append('echo {0:s}Create _testlang.test1.pot{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('xgettext{0:s} -L python -d gui -o {1:s} {2:s}{3:s}'.format(_ext, _file1_pot, _file1_py,
                                                                                    _newline))
            _ret.append('echo {0:s}Create _testlang.test1.tester.pot{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('xgettext{0:s} -L python -d gui -o {1:s} {2:s}{3:s}'.format(_ext, _file2_pot, _file2_py,
                                                                                    _newline))

            _ret.append('echo {0:s}Merge gui.pot{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('msgcat{0:s} {1:s} {2:s} -o {3:s}{4:s}'.format(_ext, _file1_pot, _file2_pot,
                                                                       _domain_pot, _newline))

        if command == "copy":
            _ret.append('echo {0:s}Update en/gui{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('{0:s} {1:s} {2:s}{3:s}'.format(_copy, _domain_pot, _po_en, _newline))
            _ret.append('echo {0:s}Update de/gui{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('{0:s} {1:s} {2:s}{3:s}'.format(_copy, _domain_pot, _po_de, _newline))

        if command == "update":
            _ret.append('echo {0:s}Update en/gui{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('msgmerge{0:s} -N -U {1:s} {2:s}{3:s}'.format(_ext, _po_en, _domain_pot, _newline))
            _ret.append('echo {0:s}Update de/gui{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('msgmerge{0:s} -N -U {1:s} {2:s}{3:s}'.format(_ext, _po_de, _domain_pot, _newline))

        if command == "compile":
            _ret.append('echo {0:s}Compile en/gui{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('msgfmt{0:s} -o {1:s} {2:s}{3:s}'.format(_ext, _mo_en, _po_en, _newline))
            _ret.append('echo {0:s}Compile de/gui{0:s}{1:s}'.format(_echo, _newline))
            _ret.append('msgfmt{0:s} -o {1:s} {2:s}{3:s}'.format(_ext, _mo_de, _po_de, _newline))

        return _ret

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
        _checklist = _parser.generate()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="generate")

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 6, "_parser.length != 6")
        self.assertListEqual(_testlist, _checklist)
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
        _checklist = _parser.generate()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="generate", is_windows=True)

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 6, "_parser.length != 6")
        self.assertListEqual(_testlist, _checklist)
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
        _checklist = _parser.copy()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="copy")

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 4, "_parser.length != 4")
        self.assertListEqual(_testlist, _checklist)
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
        _checklist = _parser.copy()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="copy", is_windows=True)

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 4, "_parser.length != 4")
        self.assertListEqual(_testlist, _checklist)
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
        _checklist = _parser.update()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="update")

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 4, "_parser.length != 4")
        self.assertListEqual(_testlist, _checklist)
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
        _checklist = _parser.update()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="update", is_windows=True)

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 4, "_parser.length != 4")
        self.assertListEqual(_testlist, _checklist)
        return

    # noinspection PyUnresolvedReferences
    def test_compile_01(self):
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
        _checklist = _parser.compile()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="compile")

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 4, "_parser.length != 4")
        self.assertListEqual(_testlist, _checklist)
        return

    # noinspection PyUnresolvedReferences
    def test_compile_02(self):
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
        _checklist = _parser.compile()
        _length = len(_checklist)

        _testlist = self._create_test_list(command="compile", is_windows=True)

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_length, 4, "_parser.length != 4")
        self.assertListEqual(_testlist, _checklist)
        return

    # noinspection PyUnresolvedReferences
    @mock.patch('builtins.open', new=mock_store_generate_01)
    def test_store_generate_01(self):
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

        _file1_out = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file1_in = full_path("{0:s}/testdata/testlang/test1/__init__.py".format(_root))

        _file2_out = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file2_in = full_path("{0:s}/testdata/testlang/test1/tester.py".format(_root))

        _file_out = full_path("{0:s}/.locales/gui/gui.pot".format(_root))

        _check3 = _parser.store_generate()

        _args = mock_store_generate_01.return_value.write.call_args_list
        _arg_list = []

        for _call in _args:
            _item = _call.args[0]
            _arg_list.append(_item)

        _lines = [
            '#!/bin/bash\n',
            'echo "Create _testlang.test1.pot"\n',
            'xgettext -L python -d gui -o {0:s} {1:s}\n'.format(_file1_out, _file1_in),
            'echo "Create _testlang.test1.tester.pot"\n',
            'xgettext -L python -d gui -o {0:s} {1:s}\n'.format(_file2_out, _file2_in),
            'echo "Merge gui.pot"\n',
            'msgcat {0:s} {1:s} -o {2:s}\n'.format(_file1_out, _file2_out, _file_out)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_check3, True, "_check2 != True")
        self.assertListEqual(_lines, _arg_list)
        return

    # noinspection PyUnresolvedReferences
    @mock.patch('builtins.open', new=mock_store_generate_02)
    def test_store_generate_02(self):
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

        _file1_out = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file1_in = full_path("{0:s}/testdata/testlang/test1/__init__.py".format(_root))

        _file2_out = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file2_in = full_path("{0:s}/testdata/testlang/test1/tester.py".format(_root))

        _file_out = full_path("{0:s}/.locales/gui/gui.pot".format(_root))

        _check3 = _parser.store_generate()

        _args = mock_store_generate_02.return_value.write.call_args_list
        _arg_list = []

        for _call in _args:
            _item = _call.args[0]
            _arg_list.append(_item)

        _lines = [
            '@echo off\n',
            'echo Create _testlang.test1.pot\n',
            'xgettext.exe -L python -d gui -o {0:s} {1:s}\n'.format(_file1_out, _file1_in),
            'echo Create _testlang.test1.tester.pot\n',
            'xgettext.exe -L python -d gui -o {0:s} {1:s}\n'.format(_file2_out, _file2_in),
            'echo Merge gui.pot\n',
            'msgcat.exe {0:s} {1:s} -o {2:s}\n'.format(_file1_out, _file2_out, _file_out)
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_check3, True, "_check2 != True")
        self.assertListEqual(_lines, _arg_list)
        return

    # noinspection PyUnresolvedReferences
    @mock.patch('builtins.open', new=mock_store_generate_03)
    def test_store_generate_03(self):
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

        _file1_out = full_path("{0:s}/.locales/gui/_testlang.test1.pot".format(_root))
        _file1_in = full_path("{0:s}/testdata/testlang/test1/__init__.py".format(_root))

        _file2_out = full_path("{0:s}/.locales/gui/_testlang.test1.tester.pot".format(_root))
        _file2_in = full_path("{0:s}/testdata/testlang/test1/tester.py".format(_root))

        _file_out = full_path("{0:s}/.locales/gui/gui.pot".format(_root))

        _check1 = _parser.store_generate()

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, False, "_check1 != False")
        self.assertEqual(_check2, True, "_check2 != True")
        return

    # noinspection PyUnresolvedReferences
    @mock.patch('builtins.open', new=mock_store_update_01)
    def test_store_update_01(self):
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
        _check3 = _parser.store_update()

        _args = mock_store_update_01.return_value.write.call_args_list
        _arg_list = []

        for _call in _args:
            _item = _call.args[0]
            _arg_list.append(_item)

        _pot = full_path("{0:s}/.locales/gui/gui.pot".format(_root))
        _po_en = full_path("{0:s}/tests/locales/en/LC_MESSAGES/gui.po".format(_root))
        _po_de = full_path("{0:s}/tests/locales/de/LC_MESSAGES/gui.po".format(_root))

        _lines = [
            '#!/bin/bash\n',
            'echo "Update en/gui"\n',
            'msgmerge -N -U {0:s} {1:s}\n'.format(_po_en, _pot),
            'echo "Update de/gui"\n',
            'msgmerge -N -U {0:s} {1:s}\n'.format(_po_de, _pot),
        ]

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_check3, True, "_check2 != True")
        self.assertListEqual(_lines, _arg_list)
        return

    # noinspection PyUnresolvedReferences
    @mock.patch('builtins.open', new=mock_store_update_02)
    def test_store_update_02(self):
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
        _check3 = _parser.store_update()

        self.assertNotEqual(_parser, None, "_parser: None")
        self.assertEqual(_check1, True, "_check1 != True")
        self.assertEqual(_check2, True, "_check2 != True")
        self.assertEqual(_check3, False, "_check2 != False")
        return
