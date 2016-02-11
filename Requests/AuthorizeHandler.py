import tornado.web
from Requests.Generic.GenericHandler import GenericHandler


class handler(GenericHandler):
    def get(self):
        machine = self.get_argument("machine")
        user = self.get_argument("user")
        auth = self.get_argument("auth")

        self.check_machine_exists(machine)
        self.check_user_exists(user)
        self.check_user_exists(auth)
        self.check_user_isauth(auth)
        
        self.auth.authorize_user(self.auth.get_machine(machine),
                                 self.auth.get_user(user))
                                 
        if self.auth.user_authorized(self.auth.get_machine(machine),
                                     self.auth.get_user(user)):
            self.write("TRUE")
        else:
            self.write("FALSE")
