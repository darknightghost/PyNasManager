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
    Module to handle config.
    
    Format of config file:
        <?xml version="1.0" encoding="utf-8"?>
        <ServerConfig>
            <key name="system" value="">
                <key name="sql-uri" value="" />
                ...
            </key>"
            <key name="modules" value="mudules">
                <key name="module-name" value="">
                    ...
                </key>
                ...
            </key>
        </ServerConfig>
'''

import xml
import os

class Config:
    '''
        Config class.
    '''
    class Key:
        '''
            Config key.
        '''
        def __init__(self, key, value, parent = None):
            self.__key = key
            self.__value = value
            self.__children = {}
            self.__parent = parent

        def parent(self):
            return self.__parent

        def set_parent(self, parent):
            self.__parent = parent

        def name(self):
            return self.name

        def set_name(self, new_name):
            self.__name = new_name

        def value(self):
            return self.value

        def set_value(self, new_value):
            self.__value = new_value

        def child(self, key):
            return self.__children[key]

        def set_child(self, key, node):
            if node.parent != None:
                raise ValueError("Node has already been used.")

            self.__children[key] = node
            node.set_parent(self)
            node.set_name(key)

        def remove_child(self, key):
            self.__children[key].set_parent(None)
            del self.__children[key]

        def __get_key(self, path):
            #Get the begining node
            current_node = self
            if path[0] == '/':
                while current_node.parent() != None:
                    current_node = current_node.parent()

            #Get key
            names = path.split("/")
            for n in names:
                if n in (".", ""):
                    continue

                elif n == "..":
                    current_node = current_node.parent()

                else:
                    current_node = current_node.child(n)

                if current_node == None:
                    raise KeyError("Illegal path \"%s\"."%(path))

            return current_node


        def __getitem__(self, path):
            return self.__get_child(path)

        def __setitem__(self, path, node):
            key = path.split("/")[-1]
            if key == "":
                raise KeyError("Illegal path \"%s\"."%(path))

            parent = self.__get_key(path[: -len(key)])
            parent.set_child(key, node)

        def __delitem__(self, key):
            key = path.split("/")[-1]
            if key == "":
                raise KeyError("Illegal path \"%s\"."%(path))

            parent = self.__get_key(path[: -len(key)])
            parent.remove_child(key)

        def load(self, node):
            pass

        def save(self):
            pass

    def __init__(self,
            path=os.path.join(os.path.dirname(__file__), "config.xml")):
        self.path = os.path.abspath(path)

    def load(self):
        pass

    def save(self):
        pass

    def root(self):
        pass
