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

import bbutil
from bbutil.utils import full_path

from tests.helper import set_log, set_module
from tests.helper.config import MockArgumentParser01, MockArgumentParser02, MockArgumentParser03

from testdata.app.config import AppConfig

__all__ = [
    "TestConfig"
]

oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()


class TestConfig(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        set_module()
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser01)
    def test_init_01(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertTrue(_check2)
        self.assertEqual(_config.verbose, 0)
        self.assertEqual(_config.bla, "/usr/local/bin/bla")
        self.assertEqual(_config.bleb, 10)
        self.assertEqual(_config.ls, "/usr/bin/ls")
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser01)
    def test_init_02(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=False)

        _check2 = _config.init()
        self.assertTrue(_check2)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser01)
    def test_init_03(self):
        bbutil.module = None
        bbutil.set_module(None)
        self.assertIsNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser02)
    def test_init_04(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        return

    @mock.patch('argparse.ArgumentParser', new=MockArgumentParser03)
    def test_init_05(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_parser=True)

        _check2 = _config.init()
        self.assertFalse(_check2)
        return

    def test_init_06(self):
        self.assertIsNotNone(bbutil.module)

        _filename = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))
        _config = AppConfig(use_config=True, config_filename=_filename)

        _check2 = _config.init()
        self.assertTrue(_check2)
        self.assertEqual(_config.verbose, 0)
        self.assertEqual(_config.bla, "/usr/local/bin/bla")
        self.assertEqual(_config.bleb, 10)
        self.assertEqual(_config.ls, "/usr/bin/ls")
        return

    def test_init_07(self):
        self.assertIsNotNone(bbutil.module)

        _config = AppConfig(use_config=True, config_filename="pufffy")

        _check2 = _config.init()
        self.assertFalse(_check2)
        return

    def test_init_08(self):
        self.assertIsNotNone(bbutil.module)

        _filename = full_path("{0:s}/testdata/config02.json".format(os.getcwd()))
        _config = AppConfig(use_config=True, config_filename=_filename)

        _check2 = _config.init()
        self.assertFalse(_check2)
        return