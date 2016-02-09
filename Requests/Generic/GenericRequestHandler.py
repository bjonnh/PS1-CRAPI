import tornado.web

class GenericRequestHandler(tornado.web.RequestHandler):
    """Authorization Request Handler, gets machine and user as argument
    returns TRUE or FALSE according to authorization status
    if machine doesn't exist returns ERR_MACHINE_NOT_REGISTERED,
    if user doesn't exist returns ERR_USER_NOT_REGISTERED
    """
    def initialize(self, auth):
        self.auth = auth

    def check(self):
        try:
            machine = self.get_argument("machine")
            user = self.get_argument("user")
        except tornado.web.MissingArgumentError:
            self.write("ERR_INVALID_REQUEST")
            return None

        if not self.auth.machine_registered(machine):
            self.write("ERR_MACHINE_NOT_REGISTERED")
            return None

        if not self.auth.user_registered(user):
            self.write("ERR_USER_NOT_REGISTERED")
            return None

        if self.auth.user_authorized(self.auth.get_machine(machine),
                                     self.auth.get_user(user)):
            self.write("TRUE")
        else:
            self.write("FALSE")

