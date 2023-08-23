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

__all__ = [
]

from dataclasses import dataclass
from typing import List

import bbutil
from bbutil.utils import get_attribute
from bbutil.worker import Worker


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
