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

import sys
from dataclasses import dataclass, asdict

import bbutil

from bbutil.app.config import Config

from bbutil.utils import check_object, check_dict, full_path

__all__ = [
    "AppConfig"
]

if sys.platform == "win32":
    _ls = "dir.bat"
else:
    _ls = "/usr/bin/ls"


@dataclass
class AppConfig(Config):

    bla: str = ""
    ls: str = ""
    bleb: int = 0
    work: str = ""

    def setup_parser(self):
        self.parser.add_argument("-b", "--bla", help="bla binary", type=str, default="/usr/bin/bla")
        self.parser.add_argument("-e", "--bleb", help="bleb settings", type=int, default=5)
        self.parser.add_argument("-l", "--ls", help="bleb settings", type=str, default=_ls)
        self.parser.add_argument("-w", "--work", help="work folder", type=str, default="test")
        return

    def read_parser(self, options) -> bool:
        _check = check_object(options, ["bla", "bleb", "ls", "work"])
        if _check is False:
            bbutil.log.error("Parser arguments are not complete!")
            return False

        self.bla = options.bla
        self.bleb = options.bleb
        self.ls = options.ls
        self.work = full_path(options.work)
        return True

    def parse_config(self, config: dict) -> bool:
        _check = check_dict(config, ["bla", "bleb", "ls", "work"])
        if _check is False:
            bbutil.log.error("Config is not complete!")
            return False
        self.bla = config["bla"]
        self.bleb = config["bleb"]
        self.ls = config["ls"]
        self.work = full_path(config["work"])
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

        check = self.check_path(self.work)
        if check is False:
            return False
        return True

    def create_config(self) -> dict:
        _config = {
            "bla": self.bla,
            "bleb": self.bleb,
            "ls": self.ls,
            "work": self.work,
            "verbose": self.verbose
        }
        return _config
