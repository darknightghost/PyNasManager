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
import flask
import web    
import Application

app = Application.Application()

@app.app.route("/login.html", methods=['GET'])
def login():
    global app

    if "error" in flask.request.args:
        error = flask.request.args["error"]
        return flask.render_template_string(web.load_template(__file__), error = error)

    else:
        return flask.render_template_string(web.load_template(__file__))


@app.app.route("/do-login.html", methods=['POST'])
def do_login():
    return ""

