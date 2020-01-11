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


import unittest

from bbutil.data import Data, Convert

members = [
    "A",
    "B",
    "name",
    "lola"
]

values = [
    0.01,
    10,
    "Lola",
    False
]

values2 = [
    0.01,
    10,
    False
]


data1 = {
    "ConfigDriver": {
        "id": "Driver.PSQL",
        "name": "PSQL",
        "count": 0,
        "temp": 0.0,
        "check": False,
        "lola": [
            1,
            2,
            "012",
            "y012",
            {
                "alpha": 0,
                "beta": "1"
            }
        ],
        "desc": "PostgreSQL database",
        "connection": {
            "name": "PSQLConnector",
            "path": "bbdata.driver.psql"
        },
        "driver": {
            "name": "PSQLWorker",
            "path": "bbdata.driver.psql"
        }
    }
}


data2 = {
    "Config.Driver": {
        "id": "Driver.PSQL",
        "name": "PSQL",
        "count": 0,
        "temp": 0.0,
        "check": False,
        "lola": [
            1,
            2,
            "012",
            "y012",
            {
                "alpha": 0,
                "beta": "1"
            }
        ],
        "desc": "PostgreSQL database",
        "connection": {
            "name": "PSQLConnector",
            "path": "bbdata.driver.psql"
        },
        "driver": {
            "name": "PSQLWorker",
            "path": "bbdata.driver.psql"
        }
    }
}


data3 = {
    "ConfigDriver": {
        "id": "Driver.PSQL",
        "name": "PSQL",
        "count": None,
        "temp": 0.0,
        "check": False,
        "lola": [
            1,
            2,
            "012",
            "y012",
            {
                "alpha": 0,
                "beta": "1"
            }
        ],
        "desc": "PostgreSQL database",
        "connection": {
            "name": "PSQLConnector",
            "path": "bbdata.driver.psql"
        },
        "driver": {
            "name": "PSQLWorker",
            "path": "bbdata.driver.psql"
        }
    }
}


class TestData(unittest.TestCase):
    """Testing class for locking module."""

    def setUp(self):
        return

    def tearDown(self):
        return

    # noinspection PyUnresolvedReferences
    def test_constructor_01(self):
        data = Data(id="Config.Test",
                    keys=members,
                    values=values)

        self.assertNotEqual(data, None, "BaseData: None")
        self.assertEqual(data.A, 0.01, "config.A: 0.01")
        self.assertEqual(data.B, 10, "config.B: 10")
        self.assertEqual(data.name, "Lola", "config.name: Lola")
        self.assertEqual(data.lola, False, "config.lola: False")
        self.assertEqual(str(data), "Config.Test", "data: Config.Test")
        return

    def test_constructor_02(self):
        data = Data(id="Config.Test",
                    values=values2)

        self.assertNotEqual(data, None, "BaseData: None")
        return

    def test_constructor_03(self):
        data = Data(id="Config.Test",
                    keys=members,
                    values=values2)

        self.assertNotEqual(data, None, "BaseData: None")
        return


class TestConvert(unittest.TestCase):
    """Testing class for ConvertPlain module."""

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_constructor(self):
        convert = Convert()
        self.assertIsNotNone(convert)
        return

    def test_parse_01(self):
        json = data1
        convert = Convert()

        data = convert.parse(json)

        self.assertIsNot(data, None)
        self.assertIsNot(data.ConfigDriver, None)
        self.assertEqual(str(data.ConfigDriver), "ConfigDriver")
        self.assertEqual(data.ConfigDriver.id, "Driver.PSQL")
        self.assertEqual(data.ConfigDriver.name, "PSQL")
        self.assertEqual(data.ConfigDriver.count, 0)
        self.assertEqual(data.ConfigDriver.temp, 0.0)
        self.assertEqual(data.ConfigDriver.check, False)
        self.assertIsNot(data.ConfigDriver.lola, None)
        self.assertEqual(len(data.ConfigDriver.lola), 5)
        self.assertEqual(data.ConfigDriver.desc, "PostgreSQL database")
        self.assertIsNot(data.ConfigDriver.connection, None)
        self.assertEqual(data.ConfigDriver.connection.name, "PSQLConnector")
        self.assertEqual(data.ConfigDriver.connection.path, "bbdata.driver.psql")
        self.assertIsNot(data.ConfigDriver.driver, None)
        self.assertEqual(data.ConfigDriver.driver.name, "PSQLWorker")
        self.assertEqual(data.ConfigDriver.driver.path, "bbdata.driver.psql")
        return

    def test_parse_02(self):
        json = data2
        convert = Convert()
        self.assertRaises(ValueError, convert.parse, json)
        return

    def test_parse_03(self):
        json = data1
        convert = Convert()

        # noinspection PyTypeChecker
        json['count'] = (0, 0, 0)

        data = convert.parse(json)
        self.assertEqual(len(data.count), 3)
        return

    def test_parse_04(self):
        json = data1
        convert = Convert()

        # noinspection PyTypeChecker
        json['ConfigDriver']['count'] = None

        data = convert.parse(json)

        self.assertIsNotNone(data)
        self.assertEqual(data.ConfigDriver.count, None)
        return

    def test_parse_05(self):
        convert = Convert()

        data = convert.parse(data3)

        self.assertIsNotNone(data)
        self.assertEqual(data.ConfigDriver.count, None)
        return
