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
import os.path
import gettext

from typing import Dict, Optional, Any, List

__all__ = [
    "Domain",
    "Lang"
]

lang_domain = None


class Domain(object):

    def __init__(self, localedir: str, domain: str, use_dummy: bool, ignore, used_lang: str):
        self.localedir: str = localedir
        self.domain: str = domain
        self.gettext: Optional[gettext.translation] = None
        self.lang = None
        self.is_set: bool = False
        self.ignore = ignore
        self.callback: List[Any] = []
        self.used_lang: str = used_lang
        self.use_dummy: bool = use_dummy
        return

    @staticmethod
    def _dummy(text: str):
        return text

    def create(self):
        if self.is_set is True:
            return

        if self.ignore is not None:
            self.use_dummy = True

        if self.use_dummy is True:
            self.lang = self._dummy
            self.is_set = True
            return

        used_catalog = [
            self.used_lang
        ]

        self.gettext = gettext.translation(self.domain, localedir=self.localedir, languages=used_catalog)
        self.gettext.install()

        self.lang = self.gettext.gettext
        self.is_set = True
        return

    def load(self):
        for _callback in self.callback:
            _callback(self.lang)
        return


class Lang(object):

    def __init__(self):
        self.localedir: Optional[str] = None
        self.do_setup: bool = False
        self.used_lang: Optional[str] = None
        self.ignore = os.getenv("IGNORE_GETTEXT", None)
        self.domains: Dict[str, Domain] = {}
        self.use_dummy: bool = False
        self.is_setup: bool = False
        return

    @staticmethod
    def dummy(text: str):
        return text

    def setup(self, localedir: str, used_lang: str = "en") -> bool:
        self.is_setup = False
        if localedir == "":
            return False

        if os.path.exists(localedir) is False:
            self.use_dummy = True
            return False

        self.localedir = localedir

        if self.used_lang is None:
            self.used_lang = used_lang

        if self.ignore is not None:
            self.use_dummy = True
        self.is_setup = True
        return True

    def _get_domain(self, domain: str) -> Optional[Domain]:

        try:
            _domain = self.domains[domain]
        except KeyError:
            return None

        return _domain

    def _create_domain(self, domain: str) -> Domain:
        _domain = Domain(localedir=self.localedir,
                         domain=domain,
                         use_dummy=self.use_dummy,
                         ignore=self.ignore,
                         used_lang=self.used_lang)

        self.domains[_domain.domain] = _domain
        return _domain

    def set_language(self, language: str):
        self.used_lang = language

        for _name in self.domains:
            _domain = self.domains[_name]
            _domain.used_lang = self.used_lang
            _domain.create()
            _domain.load()
        return

    def add(self, domain: str, callback: Any = None):

        _domain = self._get_domain(domain)
        if _domain is None:
            _domain = self._create_domain(domain)
            _domain.create()

        _domain.callback.append(callback)
        _domain.load()
        return
