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

from typing import Optional, List

import bbutil
from bbutil.utils import get_attribute
from bbutil.worker import Worker

__all__ = [
    "Module"
]


class Module(object):

    def __init__(self):
        self.name: str = ""
        self.path: str = ""

        self.command: str = ""
        self.desc: str = ""
        self.workers: List[Worker] = []
        self._module = None
        return

    def get_worker(self, worker_id: str) -> Optional[Worker]:
        for _worker in self.workers:
            if _worker.id == worker_id:
                return _worker
        return None

    def init(self, path: str, name: str) -> bool:
        self.name = name
        self.path = "{0:s}.{1:s}".format(path, name)

        try:
            _module = get_attribute(path, name)
        except ImportError as e:
            bbutil.log.exception(e)
            return False

        if hasattr(_module, "__command__") is False:
            bbutil.log.error("No commands for {0:s}!".format(name))
            return False

        if hasattr(_module, "__desc__") is False:
            bbutil.log.error("No description for {0:s}!".format(name))
            return False

        self.command = _module.__command__
        self.desc = _module.__desc__

        self._module = _module
        return True

    def load(self) -> bool:

        _worker_list = self._module.__all__

        for item in _worker_list:
            _path = "{0:s}.{1:s}".format(self.path, item)

            try:
                _name = get_attribute(_path, "__worker__")
            except ImportError as e:
                bbutil.log.error("Unable to get worker name!")
                bbutil.log.exception(e)
                return False

            try:
                c = get_attribute(_path, _name)
            except ImportError as e:
                bbutil.log.error("Unable to get worker class!")
                bbutil.log.exception(e)
                return False

            _worker = c()
            self.workers.append(_worker)
        return True
