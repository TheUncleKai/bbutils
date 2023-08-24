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

from dataclasses import dataclass, asdict

import bbutil

from bbutil.app.config import Config

from bbutil.utils import check_object, check_dict

__all__ = [
    "AppConfig"
]


@dataclass
class AppConfig(Config):

    bla: str = ""
    ls: str = ""
    bleb: int = 0

    def setup_parser(self):
        self.parser.add_argument("-b", "--bla", help="bla binary", type=str, default="/usr/bin/bla")
        self.parser.add_argument("-e", "--bleb", help="bleb settings", type=int, default=5)
        self.parser.add_argument("-l", "--ls", help="bleb settings", type=str, default="/usr/bin/ls")
        return

    def read_parser(self, options) -> bool:
        _check = check_object(options, ["bla", "bleb", "ls"])
        if _check is False:
            bbutil.log.error("Parser arguments are not complete!")
            return False

        self.bla = options.bla
        self.bleb = options.bleb
        self.ls = options.ls
        return True

    def parse_config(self, config: dict) -> bool:
        _check = check_dict(config, ["bla", "bleb", "ls"])
        if _check is False:
            bbutil.log.error("Config is not complete!")
            return False
        self.bla = config["bla"]
        self.bleb = config["bleb"]
        self.ls = config["ls"]
        return True

    def check_config(self) -> bool:
        if self.bla == "":
            bbutil.log.error("bla is missing!")
            return False

        if self.bleb < 0:
            bbutil.log.error("bleb is invalid!")
            return False
        check = self.check_path(self.ls)
        if check is False:
            return False
        return True

    def create_config(self) -> dict:
        _config = asdict(self)
        return _config
