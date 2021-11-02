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

from typing import Optional, List, TextIO
from enum import Enum

from bbutil.lang.parser.domain import Domain
from bbutil.lang.parser.language import Languages

from bbutil.utils import full_path
from bbutil.lang.parser.pyfile import PythonFile
from bbutil.logging import Logging

__all__ = [
    "pyfile",
    "domain",
    "language",

    "Command",
    "Parser"
]

log: Optional[Logging] = None


def set_log(logging: Logging):
    global log
    log = logging
    return


class Command(Enum):

    generate = "Generate"
    update = "Update"
    copy = "Copy"
    compile = "Compile"


class Parser(object):

    def __init__(self):
        self._ext: str = ""
        self._echo: str = '"'
        self._is_windows: bool = False

        self._root_path: str = os.getcwd()
        self._package_path: str = os.getcwd()
        self._module: str = ""
        self._module_filter: str = ""

        self._script: List[str] = []
        self._locales: str = ""

        self._python_files: List[PythonFile] = []
        self._domains: List[Domain] = []

        os.environ["IGNORE_GETTEXT"] = "True"
        return

    @property
    def file_number(self) -> int:
        return len(self._python_files)

    def setup(self, **kwargs) -> bool:
        item = kwargs.get("root_path", None)
        if item is not None:
            self._root_path = item

        item = kwargs.get("package_path", None)
        if item is not None:
            self._package_path = item

        item = kwargs.get("module", None)
        if item is not None:
            self._module = item

        item = kwargs.get("filter", None)
        if item is not None:
            self._module_filter = item

        item = kwargs.get("windows", None)
        if item is not None:
            if item is True:
                self._is_windows = item
                self._ext = ".exe"
                self._echo = ""

        item = kwargs.get("script", None)
        if item is not None:
            self._script = item

        item = kwargs.get("locales", None)
        if item is not None:
            self._locales = item

        if (self._module == "") or (self._locales == ""):
            log.error("Need module name or locales path!")
            return False

        return True

    def get_domain(self, domain_name: str) -> Optional[Domain]:

        for _domain in self._domains:
            if _domain.domain == domain_name:
                return _domain

        return None

    def _parse_script(self, filename: str) -> bool:
        _package_path = os.path.dirname(filename)

        log.debug2("Parse", filename)
        _file = PythonFile(package_path=_package_path,
                           filename=filename,
                           module="")

        check = _file.create()
        if check is True:
            self._python_files.append(_file)
        return check

    def _parse_package(self) -> bool:
        file_list = []

        log.inform("Check", self._package_path)
        for root, dirs, files in os.walk(self._package_path, topdown=True):
            for name in files:
                _filename = full_path("{0:s}/{1:s}".format(root, name))
                if "__pycache__" in _filename:
                    continue
                file_list.append(_filename)

        for _filename in file_list:
            log.debug2("Parse", _filename)
            _info = "Module: {0:s}, Filter: {1:s}".format(self._module, self._module_filter)
            log.debug2("Debug", _info)
            _file = PythonFile(package_path=self._package_path,
                               filename=_filename,
                               module=self._module,
                               module_filter=self._module_filter)
            check = _file.create()
            if check is False:
                continue

            self._python_files.append(_file)
        return True

    def parse(self) -> bool:

        if self._script != "":
            for _item in self._script:
                _file = full_path(_item)

                _check = self._parse_script(_file)
                if _check is False:
                    continue

        self._parse_package()

        for _file in self._python_files:
            _domain = self.get_domain(_file.domain)
            if _domain is None:
                _domain = Domain(root_path=self._root_path, domain=_file.domain)
                _domain.files.append(_file)
                _domain.lang.append(Languages(self._locales, 'en', _domain.domain))
                _domain.lang.append(Languages(self._locales, 'de', _domain.domain))
                self._domains.append(_domain)
            else:
                _domain.files.append(_file)

        log.inform("Files", str(len(self._python_files)))
        log.inform("Domain", str(len(self._domains)))
        return True

    def generate(self):
        script_line = []
        for _file in self._python_files:
            _pot = os.path.basename(_file.pot)

            _comment = 'echo {1:s}Create {0:s}{1:s}'.format(_pot, self._echo)
            _command = "xgettext{0:s} -L python -d {1:s} -o {2:s} {3:s}".format(self._ext,
                                                                                _file.domain,
                                                                                _file.pot,
                                                                                _file.fullname)

            script_line.append(_comment)
            script_line.append(_command)

        for _domain in self._domains:
            _pot = os.path.basename(_domain.pot)

            _comment = 'echo {1:s}Merge {0:s}{1:s}'.format(_pot, self._echo)
            _command = "msgcat{0:s}".format(self._ext)

            for _file in _domain.files:
                _command = "{0:s} {1:s}".format(_command, _file.pot)

            _command = "{0:s} -o {1:s}".format(_command, _domain.pot)

            script_line.append(_comment)
            script_line.append(_command)
        return script_line

    def copy(self):
        script_line = []
        for _domain in self._domains:
            for _lang in _domain.lang:
                _comment = 'echo {2:s}Update {0:s}/{1:s}{2:s}'.format(_lang.lang, _domain.domain, self._echo)

                if self._is_windows is True:
                    _command = "copy {0:s} {1:s}".format(_domain.pot, _lang.po)
                else:
                    _command = "cp {0:s} {1:s}".format(_domain.pot, _lang.po)

                script_line.append(_comment)
                script_line.append(_command)
        return script_line

    def update(self) -> list:
        script_line = []
        for _domain in self._domains:
            for _lang in _domain.lang:
                _comment = 'echo {2:s}Update {0:s}/{1:s}{2:s}'.format(_lang.lang, _domain.domain, self._echo)
                _command = "msgmerge{0:s} -N -U {1:s} {2:s}".format(self._ext, _lang.po, _domain.pot)

                script_line.append(_comment)
                script_line.append(_command)
        return script_line

    def compile(self) -> list:
        _root = os.getcwd()
        script_line = []

        for _domain in self._domains:
            for _lang in _domain.lang:
                _comment = 'echo {2:s}Compile {0:s}/{1:s}{2:s}'.format(_lang.lang, _domain.domain, self._echo)
                _command = "msgfmt{0:s} -o {1:s} {2:s}".format(self._ext, _lang.mo, _lang.po)
                script_line.append(_comment)
                script_line.append(_command)
        return script_line

    def _open(self, filename: str) -> Optional[TextIO]:
        if self._is_windows is True:
            script_ext = ".cmd"
            first_line = "@echo off\n"
        else:
            script_ext = ".sh"
            first_line = "#!/bin/bash\n"

        _filename = full_path("{0:s}{1:s}".format(filename, script_ext))

        try:
            f = open(_filename, "w")
        except IOError as e:
            log.exception(e)
            return None

        f.write(first_line)

        log.inform("Open", _filename)
        return f

    @staticmethod
    def _write(f: TextIO, lines: List[str]):
        for _item in lines:
            data = "{0:s}\n".format(_item)
            f.write(data)
        return

    def store(self, command: Command) -> bool:
        _name = ""

        if command is Command.generate:
            _name = "_lang-generate"

        if command is Command.update:
            _name = "_lang-update"

        if command is Command.copy:
            _name = "_lang-copy"

        if command is Command.compile:
            _name = "_lang-compile"

        f = self._open(_name)
        if f is None:
            return False

        if command is Command.generate:
            self._write(f, self.generate())

        if command is Command.update:
            self._write(f, self.update())

        if command is Command.copy:
            self._write(f, self.copy())

        if command is Command.compile:
            self._write(f, self.compile())

        f.close()
        return True
