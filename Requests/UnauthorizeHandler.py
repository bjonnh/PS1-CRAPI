import tornado.web

class handler(tornado.web.RequestHandler):
    def initialize(self, auth):
        self.auth = auth

    def get(self):
        try:
            machine = self.get_argument("machine")
            user = self.get_argument("user")
            auth = self.get_argument("auth")
        except tornado.web.MissingArgumentError:
            self.write("ERR_INVALID_REQUEST")
            return None

        if not self.auth.machine_registered(machine):
            self.write("ERR_MACHINE_NOT_REGISTERED")
            return None

        if not self.auth.user_registered(user):
            self.write("ERR_USER_NOT_REGISTERED")
            return None

        if not self.auth.user_registered(auth):
            self.write("ERR_AUTH_NOT_REGISTERED")
            return None

        if not self.auth.is_auth(self.auth.get_user(auth)):
            self.write("ERR_AUTH_NOT_AUTH")
            return None

        if auth == user:
            self.write("ERR_AUTH_IS_USER")
            return None

        self.auth.unauthorize_user(self.auth.get_machine(machine),
                                 self.auth.get_user(user))
                                 
        if not self.auth.user_authorized(self.auth.get_machine(machine),
                                         self.auth.get_user(user)):
            self.write("TRUE")
        else:
            self.write("FALSE")

