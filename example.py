#!/usr/bin/env python
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

import os
import time
from bbutil.logging import Logging


if __name__ == '__main__':

    print("\n\n\n")

    log = Logging()

    # Setup the logging, appicatio name is 'example', log level is 2
    log.setup(app="example", level=3)

    # We want console and file logging
    console = log.get_writer("console")
    fileio = log.get_writer("file")

    # file name to log to
    filename = os.path.abspath(os.path.normpath("{0:s}/run-tests.log".format(os.getcwd())))

    # setup file and console output, set filename and filler for space for readable output.
    console.setup(text_space=15)
    fileio.setup(text_space=15, filename=filename)

    # register the output
    log.register(console)
    log.register(fileio)

    # switch logging on
    log.open()

    # example 1, this will be shown with every log level
    log.inform("EXAMPLE", "example 1, this will be shown with every log level")

    # example 2, this will be shown with every log level
    log.warn("EXAMPLE", "this will be shown with every log level")

    # error example, this will be shown with every log level
    log.error("this will be shown with every log level!")

    # debug 1 example, this will be shown only with log level 1 and above
    log.debug1("DEBUG", "this will be shown only with log level 1 and above")

    # debug 2 example, this will be shown only with log level 2 and above
    log.debug2("DEBUG", "this will be shown only with log level 2 and above")

    # debug 3 example, this will be shown only with log level 3
    log.debug3("DEBUG", "this will be shown only with log level 3")

    # show exceptions, this will be shown with every log level
    log.inform("EXCEPTIONS", "this will be shown with every log level")

    try:
        _ = 1 / 0
    except ZeroDivisionError as e:
        log.exception(e)

    # show traceback, this will be shown with every log level
    log.inform("TRACEBACK", "this will be shown with every log level")
    try:
        _ = 1 / 0
    except ZeroDivisionError:
        log.traceback()

    # show a progress meter via console
    # first parameter: limit of the counter
    # second parameter: update interval
    # the update interval is there to prevent flickering, it also reduces the load
    log.inform("PROGRESS", "count from 0 to 1000 in 10 interval, set the value via set()")
    count1 = 0
    progress1 = log.progress(1000, 10)

    while True:
        progress1.set(count1)
        time.sleep(0.0001)

        count1 += 1

        if count1 > 1000:
            break

    # to remove the progress bar use clear
    log.clear()

    # it also can be used backwards
    log.inform("PROGRESS", "count from 1000 to 0 in 10 interval, set the value via set()")
    count2 = 1000
    progress2 = log.progress(1000, 10)
    progress2.counter = 1000

    while True:
        progress2.set(count2)
        time.sleep(0.0001)

        count2 -= 1

        if count2 == 0:
            break

    # to remove the progress bar use clear
    log.clear()

    # now we use inc instead of setting the value
    log.inform("PROGRESS", "count from 0 to 1000 in 10 interval, set the value via inc()")
    count3 = 0
    progress3 = log.progress(1000, 10)

    while True:
        progress3.inc()
        time.sleep(0.0001)

        count3 += 1

        if count3 > 1000:
            break

    # to remove the progress bar use clear
    log.clear()

    # Timers
    log.inform("MEASURE", "Measure time.sleep(3)")
    timer1 = log.timer("Measure something")
    time.sleep(3)
    timer1.stop()

    # close logging before exit
    log.close()

    print("\n\n\n")
