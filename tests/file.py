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

from bbutil.utils import full_path
from bbutil.file import File, Folder

from tests.helper import set_log
from tests.helper.file import create_file

__all__ = [
    "TestFile"
]

oserror = OSError("Something strange did happen!")
mock_oserror = mock.Mock(side_effect=oserror)
mock_remove = mock.Mock()


class TestFile(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        set_log()
        return

    def test_file_01(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()

        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))
        _check1 = create_file(_testfile)

        self.assertTrue(_check1)

        _file = File(path=_path, basename=_basename)

        self.assertTrue(_file.valid)
        self.assertEqual(_file.fullpath, _testfile)
        self.assertTrue(_file.exists)

        os.remove(_file.fullpath)

        self.assertFalse(_file.exists)
        return

    def test_file_02(self):
        _basename = "testfiles.txt"

        _file = File(basename=_basename)

        self.assertFalse(_file.valid)
        return

    def test_file_03(self):
        _path = os.getcwd()

        _file = File(path=_path)

        self.assertFalse(_file.valid)
        return

    def test_file_04(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()

        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))

        _file = File(path=_path, basename=_basename)

        self.assertTrue(_file.valid)

        _file.clear()

        self.assertFalse(_file.valid)
        self.assertFalse(_file.check)
        return

    def test_file_05(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()

        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))
        _file = File(path=_path, basename=_basename)

        self.assertTrue(_file.valid)
        self.assertFalse(_file.check)
        return

    def test_file_06(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()
        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))

        _file = File(path=_path, basename=_basename)

        _check1 = create_file(_testfile)
        self.assertTrue(_check1)

        self.assertTrue(_file.valid)
        self.assertTrue(_file.check)
        return

    def test_file_07(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()
        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))

        _check1 = create_file(_testfile)
        self.assertTrue(_check1)

        _file = File()

        _check2 = _file.open(_testfile)

        os.remove(_testfile)

        _check3 = _file.open(_testfile)

        self.assertTrue(_check2)
        self.assertFalse(_check3)
        return

    def test_file_08(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()
        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))

        _check = create_file(_testfile)
        self.assertTrue(_check)

        _file = File()

        _check = _file.open(_testfile)
        self.assertTrue(_check)

        _check = _file.remove()
        self.assertTrue(_check)
        return

    def test_file_09(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()
        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))

        if os.path.exists(_testfile) is True:
            os.remove(_testfile)

        _file = File(path=_path, basename=_basename)

        _check = _file.remove()
        self.assertTrue(_check)
        return

    def test_file_10(self):
        _file = File()

        _check = _file.remove()
        self.assertTrue(_check)
        return

    @mock.patch('os.remove', new=mock_oserror)
    def test_file_11(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()
        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))

        _check = create_file(_testfile)
        self.assertTrue(_check)

        _file = File()

        _check = _file.open(_testfile)
        self.assertTrue(_check)

        _check = _file.remove()
        self.assertFalse(_check)
        return

    @mock.patch('os.remove', new=mock_remove)
    def test_file_12(self):
        _basename = "testfiles.txt"
        _path = os.getcwd()
        _testfile = full_path("{0:s}/{1:s}".format(_path, _basename))

        _check = create_file(_testfile)
        self.assertTrue(_check)

        _file = File()

        _check = _file.open(_testfile)
        self.assertTrue(_check)

        _check = _file.remove()
        self.assertFalse(_check)
        return

    def test_file_13(self):
        _file = File()

        self.assertTrue(_file.init())
        self.assertTrue(_file.init())
        self.assertTrue(_file.create())
        return

    def test_folder_01(self):
        _basename = "testfolder"
        _path = os.getcwd()
        _testfolder = full_path("{0:s}/{1:s}".format(_path, _basename))

        if os.path.exists(_testfolder):
            os.rmdir(_testfolder)

        _folder = Folder(path=_path, basename=_basename)

        _check = _folder.create()
        self.assertTrue(_check)

        os.rmdir(_testfolder)
        return

    def test_folder_02(self):
        _basename = "testfolder"
        _path = os.getcwd()
        _testfolder = full_path("{0:s}/{1:s}".format(_path, _basename))

        if os.path.exists(_testfolder):
            os.rmdir(_testfolder)

        _folder = Folder(path=_path, basename=_basename)

        _check = _folder.create()
        self.assertTrue(_check)

        _check = _folder.remove()
        self.assertTrue(_check)
        return

    @mock.patch('os.rmdir', new=mock_oserror)
    def test_folder_03(self):
        _basename = "testfolder"
        _path = os.getcwd()
        _testfolder = full_path("{0:s}/{1:s}".format(_path, _basename))

        if os.path.exists(_testfolder):
            os.rmdir(_testfolder)

        _folder = Folder(path=_path, basename=_basename)

        _check = _folder.create()
        self.assertTrue(_check)

        _check = _folder.remove()
        self.assertFalse(_check)
        return

    @mock.patch('os.rmdir', new=mock_remove)
    def test_folder_04(self):
        _basename = "testfolder"
        _path = os.getcwd()
        _testfolder = full_path("{0:s}/{1:s}".format(_path, _basename))

        if os.path.exists(_testfolder):
            os.rmdir(_testfolder)

        _folder = Folder(path=_path, basename=_basename)

        _check = _folder.create()
        self.assertTrue(_check)

        _check = _folder.remove()
        self.assertFalse(_check)
        return

    @mock.patch('os.mkdir', new=mock_oserror)
    def test_folder_05(self):
        _basename = "testfolder"
        _path = os.getcwd()
        _testfolder = full_path("{0:s}/{1:s}".format(_path, _basename))

        if os.path.exists(_testfolder):
            os.rmdir(_testfolder)

        _folder = Folder(path=_path, basename=_basename)

        _check = _folder.create()
        self.assertFalse(_check)
        return

    @mock.patch('os.mkdir', new=mock_remove)
    def test_folder_06(self):
        _basename = "testfolder"
        _path = os.getcwd()
        _testfolder = full_path("{0:s}/{1:s}".format(_path, _basename))

        if os.path.exists(_testfolder):
            os.rmdir(_testfolder)

        _folder = Folder(path=_path, basename=_basename)

        _check = _folder.create()
        self.assertFalse(_check)
        return
