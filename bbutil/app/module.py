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

from dataclasses import dataclass
from typing import Optional, List

import bbutil

from bbutil.utils import get_attribute

from bbutil.worker import Worker
from bbutil.console.config import Config

__all__ = [
    "ModuleManager",

    "has_module",
    "get_module"
]


@dataclass
class ModuleManager(object):

    command_path: str = ""

    def __init__(self, name: str, module_path: str, desc: str):
        self.id: str = name
        self.desc: str = desc
        self.module_path: str = module_path
        return

    def commands(self) -> List[Worker]:

        _workers = []

        try:
            _module = __import__(self.module_path)
        except ImportError as e:
            bbutil.log.exception(e)
            return _workers

        for _item in _module.__workers__:
            _path = "{0:s}.{1:s}".format(self.module_path, _item)

        path = "{0:s}.{1:s}.command".format(__path__, self.folder)
        attr = get_attribute(path, self.class_command)
        c: Worker = attr()

        _workers.append(c)
        return _workers



def has_module(command: str) -> bool:
    import mig.commands

    for _item in mig.commands.__all__:

        path = "{0:s}.{1:s}".format(__path__, _item)
        module: Module = get_attribute(path, "module")

        if module.id == command:
            return True

    return False


def get_module(command: str) -> Optional[Module]:

    import mig.commands

    for _item in mig.commands.__all__:

        path = "{0:s}.{1:s}".format(__path__, _item)
        module: Module = get_attribute(path, "module")

        if module.id == command:
            return module

    return None
