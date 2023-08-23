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

from typing import Optional

from bbutil.utils import get_attribute

__all__ = [
    "has_module",
    "get_module"
]


def has_module(command: str) -> bool:
    import mig.commands

    for _item in mig.commands.__all__:

        path = "{0:s}.{1:s}".format(__path__, _item)
        module: Module = get_attribute(path, "module")

        if module.id == command:
            return True

    return False


def get_module(command: str) -> Optional[Module]:

    import mig.commands

    for _item in mig.commands.__all__:

        path = "{0:s}.{1:s}".format(__path__, _item)
        module: Module = get_attribute(path, "module")

        if module.id == command:
            return module

    return None
