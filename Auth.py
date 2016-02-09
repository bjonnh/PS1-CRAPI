from User import User
from Machine import Machine


class Auth:
    def __init__(self):
        self.machines = {}
        self.users = {}
        self.authorizations = {}

    def machine_registered(self, machine):
        return machine in self.machines

    def user_registered(self, user):
        return user in self.users

    def add_machine(self, name):
        if name not in self.machines:
            machine = Machine(name)
            self.machines[name] = machine
            # Not necessary, but lets put fences
            if machine not in self.authorizations:
                self.authorizations[machine] = []
        else:
            machine = self.machines[name]
        return machine

    def add_user(self, name, auth=False):
        if name not in self.users:
            user = User(name, auth)
            self.users[name] = user
        else:
            user = self.users[name]
        return user

    def is_auth(self, user):
        if user.name in self.users:
            return user.is_auth()
        else:
            return False

    def authorize_user(self, machine, user):
        if (self.user_registered(user.name) and
                self.machine_registered(machine.name)):
            if user not in self.authorizations[machine]:
                self.authorizations[machine].append(user)
            return True
        else:
            return False

    def unauthorize_user(self, machine, user):
        if (self.user_registered(user.name) and
                self.machine_registered(machine.name)):
            if user in self.authorizations[machine]:
                self.authorizations[machine].remove(user)
            return True
        else:
            return False

    def user_authorized(self, machine, user):
        if (self.user_registered(user.name) and
                self.machine_registered(machine.name)):
            if user in self.authorizations[machine]:
                return True
        else:
            return False

    def get_user(self, user):
        """Get user object from name, None if it doesn't exist"""
        return self.users.get(user, None)

    def get_machine(self, machine):
        """Get machine object from name, None if it doesn't exist"""
        return self.machines.get(machine, None)
