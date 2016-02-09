import tornado.ioloop
import tornado.web

from Auth import Auth
from Requests import AuthRequestHandler, AuthorizedHandler, AuthorizeHandler, UnauthorizeHandler

auth = Auth()
machine1 = auth.add_machine('ABC1')
user1 = auth.add_user('0001', True)
user2 = auth.add_user('0002')
auth.authorize_user(machine1, user1)


def make_app():
    return tornado.web.Application([
        (r"/auth/request",
         AuthRequestHandler.handler,
         dict(auth=auth)),
        (r"/auth/authorize",
         AuthorizeHandler.handler,
         dict(auth=auth)),
        (r"/auth/unauthorize",
         UnauthorizeHandler.handler,
         dict(auth=auth)),
        # Avoids logging an invalid request if we put logging at one point
        (r"/auth/authorized",
         AuthorizedHandler.handler,
         dict(auth=auth)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8042)
    tornado.ioloop.IOLoop.current().start()
