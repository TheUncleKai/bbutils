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
    "config_testone",
    "config_testone_xx"
]


config_testone = {
    "name": "testone",
    "command": "test01",
    "desc": "the first test",
    "workers": [
        {
            "path": "testdata.app.commands.testone.prepact",
            "classname": "Worker01"
        },
        {
            "path": "testdata.app.commands.testone.runact",
            "classname": "Worker02"
        }
    ]
}


config_testone_xx = {
    "name": "testone",
    "command": "test01",
    "desc": "the first test",
    "workers": [
        {
            "path": "testdata.appx.commands.testone.prepact",
            "classname": "Worker01"
        },
        {
            "path": "testdata.app.commands.testone.runact",
            "classname": "Worker02"
        }
    ]
}
