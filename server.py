import tornado.ioloop
import tornado.web
from Auth import Auth
from Requests import (AuthRequestHandler, AuthorizedHandler,
                      AuthorizeHandler, UnauthorizeHandler)
VERSION = "0.00"

auth = Auth()
machine1 = auth.add_machine('TESTMACHINE')
user1 = auth.add_user('TESTAUTH', True)
user2 = auth.add_user('TESTUSER')
user3 = auth.add_user('TESTUSERTOBEAUTH')
auth.authorize_user(machine1, user1)
auth.authorize_user(machine1, user2)


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("PS1-CRAPI:{}".format(VERSION))


def make_app():
    return tornado.web.Application([
        (r"/version",
         VersionHandler),
        (r"/request",
         AuthRequestHandler.handler,
         dict(auth=auth)),
        (r"/authorize",
         AuthorizeHandler.handler,
         dict(auth=auth)),
        (r"/unauthorize",
         UnauthorizeHandler.handler,
         dict(auth=auth)),
        # Avoids logging an invalid request if we put logging at one point
        (r"/authorized",
         AuthorizedHandler.handler,
         dict(auth=auth)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8042)
    tornado.ioloop.IOLoop.current().start()
