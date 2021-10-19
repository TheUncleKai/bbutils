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

from typing import Optional, List

from bbutil.utils import full_path, get_attribute
from bbutil.logging import Logging

__all__ = [
    "PythonFile",
    "Languages",
    "Domain"
]

log: Optional[Logging] = None


def set_log(logging: Logging):
    global log
    log = logging
    return


class PythonFile(object):

    def __init__(self, root_path: str, filename: str):
        self.root_path: str = root_path
        self.fullname: str = filename
        self.basename: str = os.path.basename(filename).replace(".py", "")
        self.domain: str = ""
        self.classname: str = ""
        self.pot: str = ""
        self.path: str = ""
        return

    def create(self) -> bool:

        _root = full_path("{0:s}/".format(self.root_path))
        _root = "{0:s}{1:s}".format(_root, os.path.sep)
        _filename = self.fullname.replace(_root, "")

        module_path = _filename.replace(".py", "")
        module_path = module_path.replace(os.path.sep, ".")

        if "__init__" in module_path:
            module_path = module_path.replace(".__init__", "")

        self.classname = module_path

        lang = get_attribute(module_path, "lang_domain")

        if lang is None:
            return False

        _logtext = "{0:s}: {1:s}".format(lang, self.classname)

        log.inform("Add", _logtext)
        self.domain = lang
        _pot = "{0:s}/.locales/{1:s}/_{2:s}.pot".format(self.root_path, self.domain, self.classname)
        _path = "{0:s}/.locales/{1:s}".format(self.root_path, self.domain)
        self.pot = full_path(_pot)
        self.path = full_path(_path)
        return True

    def prepare(self) -> bool:
        try:
            os.makedirs(self.path, exist_ok=True)
        except OSError as e:
            log.error("Unable to create path: {0:s}".format(self.path))
            log.exception(e)
            return False
        return True


class Languages(object):

    def __init__(self, path: str, lang: str, domain: str):
        self.domain: str = domain
        self.lang: str = lang
        self.path: str = full_path("{0:s}/{1:s}/LC_MESSAGES".format(path, lang))
        self.po: str = full_path("{0:s}/{1:s}.po".format(self.path, self.domain))
        self.mo: str = full_path("{0:s}/{1:s}.mo".format(self.path, self.domain))
        return


class Domain(object):

    def __init__(self, root_path: str, domain: str):
        self.root_path: str = root_path
        self.domain: str = domain
        self.path: str = full_path("{0:s}/.locales/{1:s}".format(self.root_path, self.domain))
        self.pot: str = full_path("{0:s}/.locales/{1:s}/{1:s}.pot".format(self.root_path, self.domain))
        self.lang: List[Languages] = []
        self.files: List[PythonFile] = []
        return


class Parser(object):

    def __init__(self):
        self.ext: str = ""
        self.is_windows: bool = False

        self.script_file: str = ""
        self.script_line: List[str] = []

        self.python_files: List[PythonFile] = []
        self.domains: List[Domain] = []
        return
