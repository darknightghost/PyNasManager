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
import argparse
import imp

import flask
import flask_sqlalchemy

import logging
import logging.handlers

import DesignMode
import DesignMode.Singleton

import Config

class StaticRouter:
    def __init__(self, path, content_type):
        self.path = path
        self.content_type = content_type

    def getFile(self):
        f = open(self.path, "rb")
        data = f.read()
        f.close()

        return data, 200, {'Content-Type': self.content_type}

class Application(DesignMode.Singleton.Singleton):
    '''
        Application object.
    '''
    STATIC_FILE_EXTNAMES = {".css" : "text/css",
            ".jpg"  : "image/jpeg",
            ".jpeg" : "image/jpeg",
            ".gif"  : "image/gif",
            ".png"  : "image/png", 
            ".bmp"  : "application/x-bmp"}
    APP_NAME = "Nas Manager"
    def __init_instance__(self, cfg_path, debug):
        #Flask
        self.app = flask.Flask(self.APP_NAME)

        #Config
        self.config = Config.Config(path = cfg_path)
        self.__host = self.config.root()["/system/network/ip"].value()
        self.__port = self.config.root()["/system/network/port"].value()

        self.__debug = debug
        
        #Log
        if debug:
            level = logging.DEBUG

        else:
            level = logging.INFO

        log_file_handler = logging.handlers.RotatingFileHandler(
                self.config.root()["/system/log/path"].value(),
                maxBytes = int(self.config.root()["/system/log/max-size"].value()),
                backupCount = int(self.config.root()["/system/log/max-num"].value()),
                encoding="utf-8")
        logging.basicConfig(
                format = "%(asctime)s|%(levelname)s|%(lineno)d|%(pathname)s|%(message)s",
                level = level)
        self.logger = logging.getLogger()
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(log_file_handler)
        self.logger.info("Service initialized.")

        #Database
        self.app.config["SQLALCHEMY_DATABASE_URI"] \
                = "sqlite:///%s"%(os.path.abspath(self.config.root()[
                    "/system/database/path"].value()))
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        self.db = flask_sqlalchemy.SQLAlchemy(self.app)

    def run(self):
        self.__scan()
        self.logger.info("Service started.")
        try:
            self.app.run(self.__host, self.__port, self.__debug)

        except KeyboardInterrupt:
            pass

        self.logger.info("Service stopped.")

        return 0

    def __scan(self):
        #Get web path
        app_dir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(app_dir, "website")

        #Scan and import
        self.__do_scan(path,path)

    def __do_scan(self, root, path):
        path = os.path.abspath(path)
        files = os.listdir(path)

        for f in files:
            if f not in (".", "..", "templates"):
                file_path = os.path.abspath(os.path.join(path, f))
                if os.path.isdir(file_path):
                    #Scan sub-directory
                    self.__do_scan(root, file_path)

                elif os.path.splitext(f)[-1].lower() == ".py":
                    #Load python files
                    imp.load_source("", file_path)

                elif os.path.splitext(f)[-1].lower() \
                        in self.STATIC_FILE_EXTNAMES.keys():
                    #Load static files
                    r = StaticRouter(file_path, 
                            self.STATIC_FILE_EXTNAMES[
                                os.path.splitext(f)[-1].lower()])
                    url = file_path[len(root) :]
                    if url[0] != "/":
                        url = "/" + url

                    self.app.add_url_rule(url, f, r.getFile)
