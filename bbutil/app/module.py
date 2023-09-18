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

from dataclasses import dataclass, field
from typing import Optional, List

import bbutil
from bbutil.utils import get_attribute
from bbutil.worker import Worker

__all__ = [
    "Module"
]


@dataclass
class _Worker(object):

    path: str = ""
    classname: str = ""


@dataclass
class Module(object):

    name: str = ""
    command: str = ""
    desc: str = ""
    workers: List[Worker] = field(default_factory=list)

    _workers: List[_Worker] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.workers)

    def get_worker(self, worker_id: str) -> Optional[Worker]:
        for _worker in self.workers:
            if _worker.id == worker_id:
                return _worker
        return None

    def __post_init__(self):
        for _conifg in self.workers:

            # noinspection PyArgumentList
            _worker = _Worker(**_conifg)

            self._workers.append(_worker)

        self.workers.clear()
        return

    def load(self) -> bool:

        for item in self._workers:

            try:
                c = get_attribute(item.path, item.classname)
            except ImportError as e:
                bbutil.log.error("Unable to get worker class!")
                bbutil.log.exception(e)
                return False

            _worker = c()
            self.workers.append(_worker)
        return True
