# Authorization request handlers for PS1-CRAPI
# Copyright (C) 2016 Pumping Station One Board
# Copyright (C) 2016 Jonathan Bisson <bjonnh-psone@bjonnh.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import tornado.web
from Requests.Generic import GenericHandler
import tornado.gen

class AuthHandler(GenericHandler):
    """A generic handler for basic security check on existence of machine,
    user and auth as valid entries"""
    def pre(self):
        self.machine = self.get_argument("machine")
        self.user = self.get_argument("user")
        self.authorizer = self.get_argument("auth")

        self.check_machine_exists(self.machine)
        self.check_user_exists(self.user)
        self.check_user_exists(self.authorizer)
        self.check_user_is_authorizer_on_machine(self.machine,
                                                 self.authorizer)


class AuthorizeHandler(AuthHandler):
    """Authorize the user"""
    def action(self):
        self.auth.authorize_user(self.machine,
                                 self.user)
                                 
        if self.auth.is_user_authorized(self.machine,
                                     self.user):
            self.write("TRUE")
        else:
            self.write("FALSE")

class UnauthorizeHandler(AuthHandler):
    """Unauthorize the user"""
    def action(self):
        self.auth.unauthorize_user(self.machine,
                                   self.user)
                                 
        if not self.auth.is_user_authorized(self.user,
                                         self.machine):
            self.write("TRUE")
        else:
            self.write("FALSE")
