# Simple server for PS1-CRAPI
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


import tornado.ioloop
import tornado.web
from Auth.DummyAuth import DummyAuth
from Requests.AuthorizedHandler import (CheckHandler,
                                        RequestHandler)
from Requests.AuthorizeHandler import (AuthorizeHandler,
                                       UnauthorizeHandler)

VERSION = "0.00"

# By default it uses the dummyauth, as there is no default data, nothing
# can really be done.
# Have a look at the tests to see how to add some dummy data.

auth = DummyAuth()


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("PS1-CRAPI:{}".format(VERSION))


def make_app(auth):
    return tornado.web.Application([
        (r"/version",
         VersionHandler),
        (r"/request",
         RequestHandler,
         dict(auth=auth)),
        (r"/authorize",
         AuthorizeHandler,
         dict(auth=auth)),
        (r"/unauthorize",
         UnauthorizeHandler,
         dict(auth=auth)),
        # Avoids logging an invalid request if we put logging at one point
        (r"/check",
         CheckHandler,
         dict(auth=auth)),
    ])

if __name__ == "__main__":
    app = make_app(auth)
    app.listen(8042)
    tornado.ioloop.IOLoop.current().start()
