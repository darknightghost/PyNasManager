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

import os

def load_template(file_name):
    path = os.path.join(os.path.dirname(file_name), "templates", 
            os.path.splitext(os.path.basename(file_name))[0]) + ".html"

    f = open(path, "r")
    data = f.read()
    f.close()

    return data
