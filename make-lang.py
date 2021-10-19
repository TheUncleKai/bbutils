#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

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
        self.parser = ArgumentParser()
        self.parser.add_argument("command", help="commands to run, use <command> -h for more help", choices=_commands)

        self.parser.add_argument("-w", "--windows", help="used on windows", action='store_true')
        self.parser.add_argument("-r", "--root", help="root path", type=str, default=os.getcwd())

        self.parser.add_argument("-l", "--locales", help="locales name", type=str, default="data/locale")
        self.parser.add_argument("-m", "--module", help="module name", type=str, default="rls")
        self.parser.add_argument("-s", "--script", help="script name", type=str, default="RLS-Tester.py")
        self.parser.add_argument("-v", "--verbose", help="increase output verbosity", type=int, default=0,
                                 choices=[0, 1, 2])

        self.lang_parser: Parser = Parser()

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

        options = self.parser.parse_args()

        if options.module is None:
            log.error("Module name is missing!")
            sys.exit(1)

        if options.script is None:
            log.error("Script name is missing!")
            sys.exit(1)

        if options.command is None:
            log.error("Command name is missing!")
            sys.exit(1)

        self.lang_parser.setup(windows=options.windows,
                               root=options.root,
                               module=options.module,
                               locales=options.locales,
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

    def prepare(self) -> bool:
        _check = self.lang_parser.parse()
        if _check is False:
            return False

        return True

    def process(self) -> bool:
        self.lang_parser.script_line.clear()
        self.lang_parser.generate()
        self.lang_parser.merge()

        if self.lang_parser.length == 0:
            log.warn("Process", "No lines for generate/merge!")
            return False

        self.list_generate = self.lang_parser.script_line

        self.lang_parser.script_line.clear()
        self.lang_parser.update()

        if self.lang_parser.length == 0:
            log.warn("Process", "No lines for update!")
            return False

        self.list_update = self.lang_parser.script_line

        self.lang_parser.script_line.clear()
        self.lang_parser.copy()

        if self.lang_parser.length == 0:
            log.warn("Process", "No lines for copy!")
            return False

        self.list_copy = self.lang_parser.script_line

        self.lang_parser.script_line.clear()
        self.lang_parser.compile()

        if self.lang_parser.length == 0:
            log.warn("Process", "No lines for compile!")
            return False

        self.list_compile = self.lang_parser.script_line
        return True

    def _write(self, filename: str, line_list: list) -> bool:
        try:
            f = open(filename, "w")
        except IOError as e:
            log.exception(e)
            return False

        f.write(self.first_line)

        for _line in line_list:
            f.write("{0:s}\n".format(_line))

        try:
            f.close()
        except IOError as e:
            log.exception(e)
            return False

        length = len(line_list)

        logtext = "{0:d} - {1:s}".format(length, filename)

        log.inform("Write", logtext)
        return True

    def close(self) -> bool:

        _filename = full_path("_lang-generate{0:s}".format(self.script_ext))
        _check = self._write(_filename, self.list_generate)
        if _check is False:
            return False

        _filename = full_path("_lang-update{0:s}".format(self.script_ext))
        _check = self._write(_filename, self.list_update)
        if _check is False:
            return False

        _filename = full_path("_lang-copy{0:s}".format(self.script_ext))
        _check = self._write(_filename, self.list_copy)
        if _check is False:
            return False

        _filename = full_path("_lang-compile{0:s}".format(self.script_ext))
        _check = self._write(_filename, self.list_compile)
        if _check is False:
            return False

        return True


if __name__ == '__main__':

    main = Main()

    ret = main.setup()
    if ret is False:
        sys.exit(1)

    ret = main.prepare()
    if ret is False:
        sys.exit(1)

    ret = main.process()
    if ret is False:
        sys.exit(1)

    ret = main.close()
    if ret is False:
        sys.exit(1)
