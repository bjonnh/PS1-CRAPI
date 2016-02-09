class User:
    def __init__(self, name, auth=False):
        self.name = name
        self.auth = auth

    def is_auth(self):
        return self.auth
