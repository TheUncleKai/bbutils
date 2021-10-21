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


class TestParser(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        return

    def tearDown(self):
        return

    # noinspection PyUnresolvedReferences
    def test_create_01(self):
        _text = _("Text")
        _text = _("Text1")
        _text = _("Text2")
        return
