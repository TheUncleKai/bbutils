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

from tests.helper import set_log
from bbutil.setup import find_data_files
from tests.helper.setup import testdata1, testdata2

__all__ = [
    "TestSetup"
]


class TestSetup(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_find_data_files_01(self):
        package_files1 = []
        package_files2 = []
        _package = find_data_files("testdata", "data", package_files1, [])
        _package = find_data_files("testdata", "data", package_files2, [".py"])

        self.assertListEqual(testdata1, package_files1)
        self.assertListEqual(testdata2, package_files2)
        return
