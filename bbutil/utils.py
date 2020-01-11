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

import os
import platform
import json
from typing import Union, Any
from typing import Tuple

__all__ = [
    "check_dict",
    "openjson",
    "get_attribute",
    "get_terminal_size"
]


def check_dict(checkdict: dict, keylist: list) -> bool:
    """Checks a dict for a list of keys.

    :param checkdict: dictionary to check.
    :type checkdict: dict

    :param keylist: list with keys to check for.
    :type keylist: list

    :returns: True if all keys are present, otherwise False.
    :rtype: bool
    """
    ret = True
    list_keys = list(checkdict)

    for key in keylist:
        if list_keys.count(key) == 0:
            ret = False

    return ret


def openjson(filename: str) -> Union[dict, None]:
    """opens a json file and performs some checks.

    :param filename: json filename.
    :type filename: str

    :returns: json instance if successfull, otherwise None.
    :rtype: json, None
    """

    f = open(filename, mode='r', encoding="utf-8")
    data = json.load(f)
    f.close()
    return data


def get_attribute(path: str, classname: str) -> Union[Any, None]:
    """Load module attribute from given path.

    :param path: module path.
    :type path: str

    :param classname: class name.
    :type classname: str

    :return: attribute or None.
    """

    fromlist = [classname]

    try:
        m = __import__(path, globals(), locals(), fromlist)
    except ImportError:
        raise ImportError("Unable to find module path: {0:s}".format(path))

    try:
        c = getattr(m, classname)
    except AttributeError:
        raise ImportError("Unable to get module attribute: {0:s} with {1:s}".format(path, classname))

    return c


def _get_terminal_size_windows() -> Tuple[int, int]:  # pragma: no cover
    try:
        import struct
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh",
                                                                                                  csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except Exception as e:
        print("Unable to get terminal size!")
        print(str(e))
        pass
    return 80, 25


def _get_terminal_size_tput() -> Tuple[int, int]:  # pragma: no cover
    """get terminal width
    src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    """
    try:
        import subprocess
        import shlex
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        ret = (cols, rows)
        return ret
    except:
        pass
    return 80, 25


# noinspection PyBroadException
def _get_terminal_size_linux() -> Tuple[int, int]:  # pragma: no cover
    # noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
    def ioctl_gwinsz(fdin):
        try:
            import fcntl
            import termios
            cr_data = struct.unpack('hh',
                                    fcntl.ioctl(fdin, termios.TIOCGWINSZ, '1234'))
            return cr_data
        except:
            pass

    cr = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
    if not cr:

        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_gwinsz(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return 80, 25
    return int(cr[1]), int(cr[0])


def get_terminal_size() -> Tuple[int, int]:  # pragma: no cover
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python

     :returns: tuple with terminal size.
     :rtype: tuple
    """
    current_os = platform.system()
    tuple_xy = (80, 40)
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()

        # needed for window's python in cygwin's xterm!
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()

    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()

    # default value
    if tuple_xy is None:
        tuple_xy = (0, 0)
    return tuple_xy
