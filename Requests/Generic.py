# Generic handlers for PS1-CRAPI
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

class HandlerExited(Exception):
    pass

class GenericHandler(tornado.web.RequestHandler):
    def initialize(self, auth):
        self.auth = auth

    @tornado.gen.coroutine
    def get(self):
        try:
            self.pre()
            self.action()
            self.post()
        except HandlerExited:
            pass

    def pre(self):
        pass

    def action(self):
        pass

    def post(self):
        pass
    
    def error(self, message):
        self.write(message)
        raise HandlerExited

    def get_argument(self, argument):
        try:
            return super().get_argument(argument)
        except tornado.web.MissingArgumentError:
            self.error("ERR_INVALID_REQUEST")
                
    def check_machine_exists(self, machine):
        if not self.auth.machine_registered(machine):
            self.error("ERR_MACHINE_NOT_REGISTERED")

    def check_user_exists(self, user):
        if not self.auth.user_registered(user):
            self.error("ERR_USER_NOT_REGISTERED")

    def check_user_is_authorizer_on_machine(self, machine, user):
        if not self.auth.is_authorizer_on_machine(machine, user):
            self.error("ERR_AUTH_NOT_AUTH")

    def check_user_notauth(self, user, auth):
        if auth == user:
            self.error("ERR_AUTH_IS_USER")
