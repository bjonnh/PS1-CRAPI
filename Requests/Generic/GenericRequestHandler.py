import tornado.web
from .GenericHandler import GenericHandler


class GenericRequestHandler(GenericHandler):
    """Authorization Request Handler, gets machine and user as argument
    returns TRUE or FALSE according to authorization status
    if machine doesn't exist returns ERR_MACHINE_NOT_REGISTERED,
    if user doesn't exist returns ERR_USER_NOT_REGISTERED
    """
            
    def check(self):
        machine = self.get_argument("machine")
        user = self.get_argument("user")
        
        if not self.auth.machine_registered(machine):
            self.error("ERR_MACHINE_NOT_REGISTERED")

        if not self.auth.user_registered(user):
            self.error("ERR_USER_NOT_REGISTERED")

        if self.auth.user_authorized(self.auth.get_machine(machine),
                                     self.auth.get_user(user)):
            self.write("TRUE")
        else:
            self.write("FALSE")

