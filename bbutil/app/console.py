#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import sys

from dataclasses import dataclass

from bbutil.logging import Logging

import mig

from mig.base import Config
from mig.base.module import has_module, get_module

__all__ = [
    "Console"
]


class _Config(Config):

    def setup_args(self):
        return

    def init_args(self, options) -> bool:
        return True

    def check_command(self) -> bool:
        return True


@dataclass
class Console(object):

    command_id: str = ""

    def _set_command(self) -> bool:

        if self.command_id == "":
            command_names = sys.argv[1:]

            for _command in command_names:
                check = has_module(_command)
                if check is False:
                    continue

                self.command_id = _command
                break

        if self.command_id == "":
            _config = _Config()
            _config.prepare_parser()
            _config.parser.print_help()
            return False

        module = get_module(self.command_id)
        if module is None:
            sys.stderr.write("Command is not known: {0:s}".format(self.command_id))
            return False

        config = module.config()
        if config is None:
            sys.stderr.write("Command config is not known: {0:s}".format(self.command_id))
            return False

        mig.set_module(module)
        mig.set_config(config)

        mig.log.debug1("Command", self.command_id)
        return True

    def setup(self) -> bool:
        _log = Logging()
        mig.set_log(_log)

        mig.log.setup(app=mig.__appname__, level=2)

        console = mig.log.get_writer("console")
        console.setup(text_space=24, error_index=["ERROR", "EXCEPTION"])
        mig.log.register(console)

        check = mig.log.open()
        if check is False:
            sys.stderr.write("\nUnable to open logging!\n")
            return False

        mig.log.debug1("Version", str(mig.__version__))
        _version = sys.version.replace('\n', '- ')
        mig.log.debug1("Python", _version)

        check = self._set_command()
        if check is False:
            return False

        check = mig.config.init()
        if check is False:
            return False

        mig.log.setup(level=mig.config.logging.verbose)
        mig.log.debug1("Command", "Command is set")
        return True

    def execute(self) -> int:

        command = mig.module.command()
        if command is None:
            sys.stderr.write("Command is not known: {0:s}".format(self.command_id))
            return False

        if command is None:
            mig.log.close()
            return 1

        _check = mig.data.start()
        if _check is False:
            return False

        ret = command.execute()

        _check = mig.data.stop()
        if _check is False:
            return False

        mig.log.close()
        return ret
