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

from bbutil.utils import full_path
from bbutil.lang.pyfile import PythonFile
from bbutil.logging import Logging

__all__ = [
    "Languages",
    "Domain",
    "Parser"
]

log: Optional[Logging] = None


def set_log(logging: Logging):
    global log
    log = logging
    return


class Languages(object):

    def __repr__(self):
        return self.lang

    def __init__(self, path: str, lang: str, domain: str):
        self.domain: str = domain
        self.lang: str = lang
        self.path: str = full_path("{0:s}/{1:s}/LC_MESSAGES".format(path, lang))
        self.po: str = full_path("{0:s}/{1:s}.po".format(self.path, self.domain))
        self.mo: str = full_path("{0:s}/{1:s}.mo".format(self.path, self.domain))
        return


class Domain(object):

    def __repr__(self):
        return self.domain

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
        self._ext: str = ""
        self._is_windows: bool = False

        self._root_path: str = os.getcwd()
        self._module: str = ""
        self._module_filter: str = ""

        self._script: str = ""
        self._locales: str = ""

        self.script_line: List[str] = []

        self._python_files: List[PythonFile] = []
        self._domains: List[Domain] = []

        os.environ["IGNORE_GETTEXT"] = "True"
        return

    @property
    def file_number(self) -> int:
        return len(self._python_files)

    @property
    def length(self) -> int:
        return len(self.script_line)

    def setup(self, **kwargs) -> bool:
        item = kwargs.get("root", None)
        if item is not None:
            self._root_path = item

        item = kwargs.get("module", None)
        if item is not None:
            self._module = item

        item = kwargs.get("filter", None)
        if item is not None:
            self._module_filter = item

        item = kwargs.get("windows", None)
        if item is not None:
            self._is_windows = item
            self._ext = ".exe"

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

    def parse(self) -> bool:
        file_list = []

        if self._script != "":
            main_file = full_path(self._script)
            if os.path.exists(main_file) is False:
                log.error("Unable to find mainfile: {0:s}".format(main_file))
                return False

            file_list.append(main_file)

        log.inform("Check", self._root_path)
        for root, dirs, files in os.walk(self._root_path, topdown=True):
            for name in files:
                _filename = full_path("{0:s}/{1:s}".format(root, name))
                if "__pycache__" in _filename:
                    continue
                file_list.append(_filename)

        for _filename in file_list:
            log.debug2("Parse", _filename)
            _file = PythonFile(root_path=self._root_path,
                               filename=_filename,
                               module=self._module,
                               module_filter=self._module_filter)
            check = _file.create()
            if check is False:
                continue

            self._python_files.append(_file)

        for _file in self._python_files:
            _domain = self.get_domain(_file.domain)
            if _domain is None:
                _domain = Domain(self._root_path, _file.domain)
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
        for _file in self._python_files:
            _check = _file.prepare()
            if _check is False:
                continue

            _pot = os.path.basename(_file.pot)

            if self._is_windows is True:
                _comment = 'echo Create {0:s}'.format(_pot)
            else:
                _comment = 'echo "Create {0:s}"'.format(_pot)

            _command = "xgettext{0:s} -L python -d {1:s} -o {2:s} {3:s}".format(self._ext,
                                                                                _file.domain,
                                                                                _file.pot,
                                                                                _file.fullname)

            self.script_line.append(_comment)
            self.script_line.append(_command)
        return

    def merge(self):
        for _domain in self._domains:
            _pot = os.path.basename(_domain.pot)

            if self._is_windows is True:
                _comment = 'echo Merge {0:s}'.format(_pot)
            else:
                _comment = 'echo "Merge {0:s}"'.format(_pot)

            _command = "msgcat{0:s}".format(self._ext)

            for _file in _domain.files:
                _command = "{0:s} {1:s}".format(_command, _file.pot)

            _command = "{0:s} -o {1:s}".format(_command, _domain.pot)

            self.script_line.append(_comment)
            self.script_line.append(_command)
        return

    def copy(self):
        for _domain in self._domains:
            for _lang in _domain.lang:
                if self._is_windows is True:
                    _comment = 'echo Update {0:s}/{1:s}'.format(_lang.lang, _domain.domain)
                else:
                    _comment = 'echo "Update {0:s}/{1:s}"'.format(_lang.lang, _domain.domain)

                if self._is_windows is True:
                    _command = "copy {0:s} {1:s}".format(_domain.pot, _lang.po)
                else:
                    _command = "cp {0:s} {1:s}".format(_domain.pot, _lang.po)

                self.script_line.append(_comment)
                self.script_line.append(_command)
        return

    def update(self):
        for _domain in self._domains:
            for _lang in _domain.lang:
                if self._is_windows is True:
                    _comment = 'echo Update {0:s}/{1:s}'.format(_lang.lang, _domain.domain)
                else:
                    _comment = 'echo "Update {0:s}/{1:s}"'.format(_lang.lang, _domain.domain)

                _command = "msgmerge{0:s} -N -U {1:s} {2:s}".format(self._ext, _lang.po, _domain.pot)

                self.script_line.append(_comment)
                self.script_line.append(_command)
        return

    def compile(self):
        _root = os.getcwd()

        for _domain in self._domains:
            for _lang in _domain.lang:
                if self._is_windows is True:
                    _comment = 'echo Compile {0:s}/{1:s}'.format(_lang.lang, _domain.domain)
                else:
                    _comment = 'echo "Compile {0:s}/{1:s}"'.format(_lang.lang, _domain.domain)

                if os.path.exists(_lang.po) is False:
                    continue

                _command = "msgfmt{0:s} -o {1:s} {2:s}".format(self._ext, _lang.mo, _lang.po)

                self.script_line.append(_comment)
                self.script_line.append(_command)
        return
