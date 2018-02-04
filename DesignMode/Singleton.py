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

class Singleton:
    __instance = None

    def __init__(cls, *args, **kw):
        pass

    def __init_instance__(self):
        raise NotImplemented

    def __new__(cls, *args, **kw):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)  
            cls.__instance.__init_instance__(*args, **kw)

        return cls.__instance 
