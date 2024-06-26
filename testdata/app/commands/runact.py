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

from typing import List
from dataclasses import dataclass, field

import bbutil

from bbutil.worker import Worker

__all__ = [
    "Worker02"
]


@dataclass
class Worker02(Worker):

    max: int = 50000
    iterate_list: List[int] = field(default_factory=list)
    do_fail: bool = False

    def init(self):
        self.set_id("Act02")
        return

    def prepare(self) -> bool:
        _max = self.max
        _range = range(0, _max)
        _progress = bbutil.log.progress(_max)

        for n in _range:
            self.iterate_list.append(n)
            _progress.inc()

        bbutil.log.clear()
        return True

    def run(self) -> bool:
        _max = len(self.iterate_list)
        _progress = bbutil.log.progress(_max)

        n = 0
        for x in self.iterate_list:
            self.iterate_list[n] = x + 1
            _progress.inc()
            n += 1

        bbutil.log.clear()
        return True

    def close(self) -> bool:
        _max = len(self.iterate_list)
        _progress = bbutil.log.progress(_max)

        n = 0
        for x in self.iterate_list:
            self.iterate_list[n] = x - 1
            _progress.inc()
            n += 1

        bbutil.log.clear()
        return True
