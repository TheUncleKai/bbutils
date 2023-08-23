#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import abc
import sys

from dataclasses import dataclass
from typing import Optional
from abc import ABCMeta

import bbutil

from bbutil.logging import Logging
from bbutil.app.manager import ModuleManager
from bbutil.app.config import Config
from bbutil.app.module import Module

__all__ = [
    "Console"
]


@dataclass
class Console(metaclass=ABCMeta):

    command_id: str = ""
    module: Optional[Module] = None

    def _set_command(self, config: Config) -> bool:

        if self.command_id == "":
            command_names = sys.argv[1:]

            for _command in command_names:
                check = bbutil.module.has_command(_command)
                if check is False:
                    continue

                self.command_id = _command
                break

        if self.command_id == "":
            config.prepare_parser()
            config.parser.print_help()
            return False

        _module = bbutil.module.get_module(self.command_id)
        if _module is None:
            sys.stderr.write("Command is not known: {0:s}".format(self.command_id))
            return False

        bbutil.set_config(config)
        self.module = _module

        bbutil.log.debug1("Console", self.command_id)
        return True

    @abc.abstractmethod
    def create_logging(self) -> Logging:
        pass

    @abc.abstractmethod
    def create_config(self) -> Config:
        pass

    @abc.abstractmethod
    def start(self) -> bool:
        pass

    @abc.abstractmethod
    def stop(self) -> bool:
        pass

    def setup(self, module_path: str) -> bool:
        _modules = ModuleManager(module_path)

        check = _modules.init()
        if check is False:
            return False

        bbutil.set_module(_modules)

        _log = self.create_logging()
        bbutil.set_log(_log)

        _version = sys.version.replace('\n', '- ')
        bbutil.log.debug1("Python", _version)

        _config = self.create_config()

        check = self._set_command(_config)
        if check is False:
            return False

        check = _config.init()
        if check is False:
            return False

        bbutil.log.setup(level=_config.verbose)
        return True

    def execute(self) -> int:

        check = self.start()
        if check is False:
            return 1

        check = self.module.load()
        if check is False:
            return 2

        for _worker in self.module.workers:
            check = _worker.execute()
            if check is True:
                continue

            return 3

        check = self.stop()
        if check is False:
            return 4

        bbutil.log.close()
        return 0
