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


@dataclass
class _Callback(object):

    start = None
    stop = None
    prepare = None
    run = None
    close = None
    abort = None

    def do_start(self):
        if self.start is None:
            return
        self.start()
        return

    def do_stop(self):
        if self.stop is None:
            return
        self.start()
        return

    def do_prepare(self):
        if self.prepare is None:
            return
        self.start()
        return

    def do_run(self):
        if self.run is None:
            return
        return

    def do_close(self):
        if self.close is None:
            return
        return

    def do_abort(self):
        if self.abort is None:
            return
        return
