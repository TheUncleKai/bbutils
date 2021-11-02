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
import os
import os.path

import bbutil.lang.parser

from bbutil.logging import Logging
from bbutil.lang.parser import Parser
from bbutil.utils import full_path

from argparse import ArgumentParser

log: Logging = Logging()

_commands = [
    "generate",
    "update",
    "merge",
    "compile",
    "all"
]


class Main(object):

    def __init__(self):
        self.argument_parser = ArgumentParser()


        self.parser: Parser = Parser()

        self.command: str = ""
        self.root_path: str = ""
        self.is_windows: bool = False
        self.verbose: int = 0
        self.script_ext: str = ""
        self.first_line: str = ""

        self.list_generate = []
        self.list_update = []
        self.list_copy = []
        self.list_compile = []
        return

    def setup(self) -> bool:
        os.environ["IGNORE_GETTEXT"] = "True"

        options = self.argument_parser.parse_args()

        if options.module is None:
            log.error("Module name is missing!")
            sys.exit(1)

        if options.script is None:
            log.error("Script name is missing!")
            sys.exit(1)

        if options.command is None:
            log.error("Command name is missing!")
            sys.exit(1)

        self.parser.setup(windows=options.windows, root=options.root, module=options.module, locales=options.locales,
                          script=options.script)

        self.root_path = options.root
        self.command = options.command
        self.is_windows = options.windows

        bbutil.lang.parser.set_log(log)

        if self.is_windows is True:
            self.script_ext = ".cmd"
            self.first_line = "@echo off\n"
        else:
            self.script_ext = ".sh"
            self.first_line = "#!/bin/bash\n"

        log.setup(app="make-lang.py", level=options.verbose)

        console = log.get_writer("console")
        console.setup(text_space=12, error_index=["ERROR", "EXCEPTION"])
        log.register(console)

        check = log.open()
        if check is False:
            sys.exit(1)

        log.inform("Command", self.command)
        log.inform("Windows", str(self.is_windows))
        log.inform("Ext", self.script_ext)
        return True

    def run(self) -> bool:
        _check = self.parser.parse()
        if _check is False:
            return False



        return True


if __name__ == '__main__':

    main = Main()

    ret = main.setup()
    if ret is False:
        sys.exit(1)

    ret = main.run()
    if ret is False:
        sys.exit(1)
