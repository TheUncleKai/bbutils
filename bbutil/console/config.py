#!/usr/bin/python3
# coding=utf-8

# Copyright (C) 2020, Siemens Healthcare Diagnostics Products GmbH
# Licensed under the Siemens Inner Source License 1.2, see LICENSE.md.

import abc
import os.path

import json

from dataclasses import dataclass
from abc import ABCMeta
from argparse import ArgumentParser
from typing import Optional

from bbutil.utils import check_dict, get_attribute, openjson

import bbutil

__all__ = [
    "Config"
]


@dataclass
class Config(metaclass=ABCMeta):

    is_gui: bool = False
    is_ready: bool = False

    filename: str = ""
    parser: ArgumentParser = ArgumentParser()

    @staticmethod
    def check_path(input_path):
        if input_path == "":
            raise ValueError("Invalid path!")
        if os.path.exists(input_path) is False:
            raise ValueError("Unable to find: {0:s}".format(input_path))
        return

    @staticmethod
    def path_exists(input_path) -> bool:
        if input_path == "":
            bbutil.log.error("Path is empty!")
            return False
        if os.path.exists(input_path) is False:
            bbutil.log.error("Unable to find: {0:s}".format(input_path))
            return False
        return True

    def prepare_parser(self):
        import mig.commands

        commands = []

        for _item in mig.commands.__all__:
            path = "mig.commands.{0:s}".format(_item)
            module = get_attribute(path, "module")
            commands.append(module.id)

        self.parser.add_argument("command", help="commands to run, use <command> -h for more help",
                                 choices=commands)

        self.parser.add_argument("-v", "--verbose", help="increase output verbosity", type=int,
                                 default=0, choices=[0, 1, 2])
        return

    @abc.abstractmethod
    def setup_args(self):
        pass

    @abc.abstractmethod
    def init_args(self, options) -> bool:
        pass

    @abc.abstractmethod
    def check_command(self) -> bool:
        pass

    def _parse_args(self) -> bool:
        options = self.parser.parse_args()

        check = self.init_args(options)
        if check is False:
            bbutil.log.error("Config init failed!")
            return False
        return True

    @abc.abstractmethod
    def prepare(self) -> Optional[dict]:
        pass

    def store(self) -> bool:
        _config = self.prepare()
        if _config is None:
            return False

        if self.filename == "":
            bbutil.log.error("No filename for storing!")
            return False

        _data = json.dumps(_config, indent=4)

        bbutil.log.inform("Config", "Store {0:s}".format(self.filename))

        try:
            f = open(file=self.filename, mode="w")
        except OSError as e:
            bbutil.log.exception(e)
            return False

        f.write(_data)
        f.close()
        return True

    def init(self) -> bool:
        check = self._load_config()
        if check is False:
            return False

        if self.is_gui is False:
            self.prepare_parser()
            self.setup_args()

            check = self._parse_args()
            if check is False:
                return False

        check = self.path_exists(self.path.source)
        if check is False:
            return False

        check = self.check_command()
        if check is False:
            mig.log.error("Config check failed!")
            return False

        self.is_ready = True
        return True
