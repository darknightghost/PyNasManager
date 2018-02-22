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

import hashlib

import flask_sqlalchemy
import Application

import Privilege
import Privilege.CrossTable

app = Application.Application()

class User(app.db.Model):
    '''
        User model.
    '''
    #Columns
    id = app.db.Column(app.db.Integer, 
            app.db.Sequence('uid_seq', start=0, increment=1),
            primary_key=True)
    name = app.db.Column(app.db.String(32), unique=True, nullable=False)
    passwd_sha512 = app.db.Column(app.db.BINARY(64), unique=False, nullable=False)
    groups = app.db.relationship("UserGroup", Privilege.CrossTable.user_group_table)

    def set_passwd(self, passwd):
        '''
            Set password.
        '''
        self.passwd_sha512 = hashlib.sha512(
                passwd.encode(encoding = 'utf-8')).digest()
        return

    def check_passwd(self, passwd):
        '''
            Check password.
        '''
        passwd_hash = hashlib.sha512(
                passwd.encode(encoding = 'utf-8')).digest()

        if passwd_hash == bytes(self.passwd_sha512):
            return True

        else:
            return False
