import tornado.web
from Requests.Generic import GenericRequestHandler

class handler(GenericRequestHandler.GenericRequestHandler):
    def get(self):
        self.check()
