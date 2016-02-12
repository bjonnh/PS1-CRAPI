# Auth module for PS1-CRAPI
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

# Read Auth_Module_Python_API.txt on which functions are required
# if you want to write your own

class DummyAuth:
    def __init__(self):
        self.machines = []
        self.users = []
        self.authorizations = {}
        self.authorizers = {}

    def machine_registered(self, machine):
        return machine in self.machines

    def user_registered(self, user):
        return user in self.users

    def add_machine(self, name):
        if name not in self.machines:
            self.machines.append(name)
            # Not necessary, but lets put fences
            if name not in self.authorizations:
                self.authorizations[name] = []
                self.authorizers[name] = []

    def add_user(self, name):
        if name not in self.users:
            self.users.append(name)
            return True
        return False

    def is_authorizer_on_machine(self, machine, user):
        if user in self.users:
            return user in self.authorizers[machine]

        return False

    def make_user_authorizer_on_machine(self, machine, user):
        if (self.machine_registered(machine) and
                self.user_registered(user)):
            if user not in self.authorizers[machine]:
                self.authorizers[machine].append(user)
                return True
        return False
        
    def authorize_user(self, machine, user):
        if (self.user_registered(user) and
                self.machine_registered(machine)):
            if user not in self.authorizations[machine]:
                self.authorizations[machine].append(user)
                return True
        return False

    def unauthorize_user(self, machine, user):
        if (self.user_registered(user) and
                self.machine_registered(machine)):
            if user in self.authorizations[machine]:
                self.authorizations[machine].remove(user)
            return True
        return False

    def is_user_authorized(self, machine, user):
        if (self.user_registered(user) and
                self.machine_registered(machine)):
            if user in self.authorizations[machine]:
                return True
        return False
