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

from bbutil.utils import full_path
from bbutil.logging import Logging
from bbutil.app import Console, Config

from testdata.app.config import AppConfig

__all__ = [
    "AppConsole"
]

_index = {
    0: ["INFORM", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    1: ["INFORM", "DEBUG1", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    2: ["INFORM", "DEBUG1", "DEBUG2", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"],
    3: ["INFORM", "DEBUG1", "DEBUG2", "DEBUG3", "WARN", "ERROR", "EXCEPTION", "TIMER", "PROGRESS"]
}


class AppConsole(Console):

    def create_logging(self) -> Logging:
        _log = Logging()
        _log.setup(app="Test", level=2, index=_index)

        console = _log.get_writer("console")
        _log.register(console)
        _log.open()
        return _log

    def create_config(self) -> Config:
        _work = "{0:s}/test".format(os.getcwd())
        if os.path.exists(_work) is False:
            os.mkdir(_work)

        _filename = full_path("{0:s}/testdata/config01.json".format(os.getcwd()))
        _config = AppConfig(use_config=True, config_filename=_filename)
        return _config

    def init(self):
        self.module_path = "testdata.app.commands"
        return

    def start(self) -> bool:
        return True

    def stop(self) -> bool:
        pass
