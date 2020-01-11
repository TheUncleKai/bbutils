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

import bbutil.utils
import bbutil.data


def create_file(filename):
    path = os.path.normpath(filename)

    if os.path.exists(path) is True:
        os.unlink(path)

    f = open(path, mode='w')
    f.write("TEST")
    f.close()

    return path


def create_folder(folder):
    path = os.path.normpath(folder)
    if os.path.exists(path) is False:
        os.mkdir(path)

    return path


store_unlink = os.unlink
store_rmdir = os.rmdir

mock_sub = mock.Mock(side_effect=ValueError('Attempting to use a port that is not open'))


class TestUtils(unittest.TestCase):
    """Testing class for modules module."""

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_check_dict_1(self):
        """Test check_dict

        :argument:
        * check for existing members.
        * return True
        """
        config = {
            "check1": 0,
            "check2": 2
        }

        check = bbutil.utils.check_dict(config, ["check1", "check2"])
        self.assertTrue(check)
        return

    def test_check_dict_2(self):
        config = {
            "check1": 0,
            "check2": 2
        }

        check = bbutil.utils.check_dict(config, ["check1", "check3"])
        self.assertFalse(check)
        return

    def test_check_object_1(self):
        config = bbutil.data.Data(keys=["check1", "check2"], values=["A", "B"])

        check = bbutil.utils.check_object(config, ["check1", "check2"])
        self.assertTrue(check)
        return

    def test_check_object_2(self):
        config = bbutil.data.Data(keys=["check1", "check2"], values=["A", "B"])

        check = bbutil.utils.check_object(config, ["check1", "check3"])
        self.assertFalse(check)
        return

    def test_check_object_3(self):
        check = bbutil.utils.check_object(None, ["check1", "check3"])
        self.assertFalse(check)
        return

    def test_execute_01(self):
        ret, code = bbutil.utils.execute("execute", ["python", "--version"])
        self.assertTrue(ret)
        self.assertEqual(code, 0)
        return

    def test_execute_02(self):
        ret, code = bbutil.utils.execute("execute", ["pythonx", "--version"])
        self.assertFalse(ret)
        self.assertEqual(code, 0)
        return

    def test_execute_03(self):
        from bbutil.logging import Logging

        log = Logging()
        log.setup(app="TEST", level=2)

        console = log.get_writer("console")
        console.setup(text_space=15, error_index=["ERROR", "EXCEPTION"])
        log.register(console)

        log.open()

        ret, code = bbutil.utils.execute("execute", ["python", "--version"], None, log)
        self.assertTrue(ret)
        self.assertEqual(code, 0)
        return

    def test_execute_04(self):
        from bbutil.logging import Logging

        log = Logging()
        log.setup(app="TEST", level=2)

        console = log.get_writer("console")
        console.setup(text_space=15, error_index=["ERROR", "EXCEPTION"])
        log.register(console)

        log.open()

        data = []

        ret, code = bbutil.utils.execute("execute", ["python", "--version"], data, log)
        self.assertEqual(len(data), 1)
        self.assertTrue(ret)
        self.assertEqual(code, 0)
        return

    @mock.patch('subprocess.Popen', new=mock_sub)
    def test_execute_05(self):
        from bbutil.logging import Logging

        log = Logging()
        log.setup(app="TEST", level=2)

        console = log.get_writer("console")
        console.setup(text_space=15, error_index=["ERROR", "EXCEPTION"])
        log.register(console)

        log.open()

        ret, code = bbutil.utils.execute("execute", ["python", "--version"], None, log)
        self.assertFalse(ret)
        self.assertEqual(code, 0)
        return

    def test_full_path(self):
        filename = "run-tests.py"

        full_path = bbutil.utils.full_path(filename)

        self.assertGreater(len(full_path), len(filename))
        self.assertNotEqual(filename, full_path)
        return

    def test_get_attribute_01(self):

        logging = bbutil.utils.get_attribute("bbutil.logging", "Logging")
        self.assertIsNotNone(logging)
        return

    def test_get_attribute_02(self):

        self.assertRaises(ImportError, bbutil.utils.get_attribute, "bbutil.loggingx", "Logging")
        return

    def test_get_attribute_03(self):

        self.assertRaises(ImportError, bbutil.utils.get_attribute, "bbutil.logging", "Loggingx")
        return
