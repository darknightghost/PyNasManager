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
import xml.dom
import xml.dom.minidom
import os

class Config:
    '''
        Config class.
    '''
    class Key:
        '''
            Config key.
        '''
        def __init__(self, key = None, value = None, parent = None, doc = None):
            '''
                Key-value pair of config.

                Config.Key(key, value) -> key
                Config.Key(parent) -> key
                Config.Key(doc) -> key
            '''
            self.__key = key
            self.__value = value
            self.__children = {}
            self.__parent = parent
            self.__node = None

            if doc == None:
                self.__doc = parent.__doc

            else:
                self.__doc = doc

        def parent(self):
            '''
                Config.Key.parent() -> parent

                Get parent key-value pair.
            '''
            return self.__parent

        def __set_parent(self, parent):
            '''
                Config.Key.set_parent(parent)

                Set new parent.
            '''
            self.__parent = parent

            if self.__parent == None:
                self.__doc = None

            else:
                self.__doc = parent.__doc

            if self.__node == None:
                self.__rebuild_node()

        def key(self):
            '''
                Config.Key.key() -> str

                Get key name.
            '''
            return self.__key

        def __set_key(self, new_key):
            '''
                Config.Key.__set_key(key)

                Set key name.
            '''
            self.__key = str(new_key)

            if self.__node != None:
                self.__node.setAttribute("name", self.__key)

        def value(self):
            '''
                Config.Key.value() -> str

                Get key value.
            '''
            return self.value

        def set_value(self, new_value):
            '''
                Config.Key.__set_value(value)

                Set key value.
            '''
            self.__value = str(new_value)

            if self.__node != None:
                self.__node.setAttribute("value", self.__value)

        def child(self, key):
            '''
                Config.Key.child(key) -> node

                Get child node by key.
            '''
            return self.__children[key]

        def __set_child(self, key, node):
            '''
                Config.Key.__set_child(key, node)

                Set child.
            '''
            if node.parent != None:
                raise ValueError("Node has already been used.")

            key = str(key)

            if key in self.__children.keys():
                raise KeyError("Key has already been used.")

            node.__set_parent(self)
            self.__children[key] = node
            node.__set_key(key)

        def __remove_child(self, key):
            '''
                Config.Key.__remove_child(key)

                Remove child.
            '''
            key = str(key)
            node = self.__children[key]
            self.__doc.removeChild(node.__node)
            node.__set_parent(None)
            del self.__children[key]

        def __get_key(self, path):
            '''
                Config.Key.__get_key(path) -> node

                Get child by path.
            '''
            #Get the begining node
            key = str(key)
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
            return self.__get_key(path)

        def __setitem__(self, path, node):
            key = path.split("/")[-1]
            if key == "":
                raise KeyError("Illegal path \"%s\"."%(path))

            parent = self.__get_key(path[: -len(key)])
            parent.__set_child(key, node)

        def __delitem__(self, key):
            key = path.split("/")[-1]
            if key == "":
                raise KeyError("Illegal path \"%s\"."%(path))

            parent = self.__get_key(path[: -len(key)])
            parent.__remove_child(key)

        def load(self, node):
            '''
                Config.key.load(node)

                Load xml node.
            '''
            if self.__parent != None:
                self.__key = node.getAttribute("name")
                self.__value = node.getAttribute("value")

            else:
                self.__key = None
                self.__value = None

            self.__node = node

            for n in node.childNodes:
                if n.nodeType == n.ELEMENT_NODE \
                        and n.nodeName == "key":
                    child = Key(parent = self)
                    child.load(node)
                    self.__set_child(child.key(), child)

        def __rebuild_node(self):
            '''
                Config.key.__rebuild_node()

                Rebuild node.
            '''
            #Check status
            if self.__parent == None or self.__node != None:
                raise RuntimeError("Illegal rebuild operation.")

            #Create element
            self.__node = self.__doc.createElement("key")
            self.__node.setAttribute("name", self.__key)
            self.__node.setAttribute("value", self.__value)

    def __init__(self,
            path=os.path.join(os.path.dirname(__file__), "config.xml")):
        self.__path = os.path.abspath(path)
        self.load()

    def load(self):
        try:
            f = open(self.__path, "r")

        except FileNotFoundError as e:
            print("Failed to open config file.")
            raise e

        self.__doc = xml.dom.minidom.parseString(f.read())
        self.__root = Key(doc = self.__doc)
        self.__root.load(self.__doc.documentElement)

    def doc(self):
        return self.__doc

    def save(self):
        try:
            f = open(self.__path, "w")

        except FileNotFoundError as e:
            print("Failed to write config file.")
            raise e

        f.write(self.__doc.toprettyxml(indent = '\t', newl = '\n',
            encoding = 'utf-8'))
        f.close()

    def root(self):
        return self.__root
