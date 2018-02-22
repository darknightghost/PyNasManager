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

import re

import Privilege.User
import Privilege.UserGroup
import Privilege.UserPrivilege

class UserSession:
    '''
        User session info.
    '''
    active_users = {}
    def __init__(self):
        self.__userModel = None

    def login(self, usrname, passwd):
        '''
            user_session.login(username, passwd) -> bool

            Login.
        '''
        if self.logined():
            self.Logout()

        model = Privilege.User.User.query.filter_by(name=usrname).first()
        if model == None:
            return False

        if not model.check_passwd(passwd):
            return False

        self.__userModel = model

        return True

    def logout(self):
        '''
            user_session.logout()

            Logout.
        '''
        self.__userModel == None

    def logined(self):
        '''
            user_session.logined() -> bool

            Test if logined.
        '''
        return self.__userModel == None

    def has_privilege(self, privilege):
        '''
            user_session.has_privilege() -> bool

            Check privilege.
        '''
        if not self.logined():
            return False

    def check_username(name):
        '''
            UserSession.check_username(name) -> bool

            Check if the name is legal.
        '''
        if re.match("[^a-z_0-9]", name) == None:
            return True

        else:
            return False


class PrivilegeMgr:
    def create_user(username):
        pass

    def remove_user(id):
        pass

