# Authorization check handlers for PS1-CRAPI
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

class GenericRequestHandler(GenericHandler):
    """Authorization Request Handler, gets machine and user as argument
    returns TRUE or FALSE according to authorization status
    if machine doesn't exist returns ERR_MACHINE_NOT_REGISTERED,
    if user doesn't exist returns ERR_USER_NOT_REGISTERED
    """
            
    def check(self):
        machine = self.get_argument("machine")
        user = self.get_argument("user")
        self.check_machine_exists(machine)
        self.check_user_exists(user)
        
        if self.auth.is_user_authorized(machine, user):
            self.write("TRUE")
        else:
            self.write("FALSE")



class CheckHandler(GenericRequestHandler):
    """This is a basic handler for a simple request."""
    def action(self):
        self.check()

class RequestHandler(GenericRequestHandler):
    """This is a basic handler for a simple request with logging
    just overload the log function to make it useful."""
    def action(self):
        self.check()
        self.log()
    def log(self):
        pass
