#! /usr/bin/env python3
#-*- coding: utf-8 -*-

#	Copyright 2018, 王思远 <darknightghost.cn@gmail.com>

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	at your option) any later version.

#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.

#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
    Check environment.
'''

import sys
import os
import importlib
import importlib.util

def check_exec(name):
    '''
        check_exec(name) -> bool

        Check application exists.
    '''
    print("Checking executable file \"%s\"..."%(name), end="")
    dirs = os.environ["PATH"].split(":")
    for d in dirs:
        path = os.path.join(d, name)
        if os.path.exists(path):
            print(" OK.")
            return True

    print(" Faied.")
    return False

def check_module(name):
    '''
        check_module(name) -> bool

        Check module exists.
    '''
    print("Checking module \"%s\"..."%(name), end="")
    if importlib.util.find_spec(name) == None:
        print(" Failed.")
        return False

    else:
        print(" OK.")
        return True

def check_library(app_name, lib_name):
    '''
        check_library(app_name, lib_name) -> bool

        Check library exists.
    '''
    pass
