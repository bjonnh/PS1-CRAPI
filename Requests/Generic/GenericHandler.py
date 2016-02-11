import tornado.web

class HandlerExited(Exception):
    pass

class GenericHandler(tornado.web.RequestHandler):
    def initialize(self, auth):
        self.auth = auth

    def get(self):
        try:
            self.action()
        except HandlerExited:
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

    def check_user_isauth(self, user):
        if not self.auth.is_auth(self.auth.get_user(user)):
            self.error("ERR_AUTH_NOT_AUTH")

    def check_user_notauth(self, user, auth):
        if auth == user:
            self.error("ERR_AUTH_IS_USER")
