import tornado.httpclient

SERVER = "http://127.0.0.1:8042"


class GenericTest:
    def generic_url_return(self, url, returnvalue):
        http_client = tornado.httpclient.HTTPClient()
        try:
            response = http_client.fetch(url)
        except tornado.httpclient.HTTPError as e:
            # This is maybe not a PS1-CRAPI server
            assert False
        except Exception as e:
            # If connection is not possible
            assert False
        return response.body

    def generic_url_return_equal(self,url,returnvalue):
        assert self.generic_url_return(url, returnvalue) == returnvalue
    def generic_url_return_startswith(self,url,returnvalue):
        assert returnvalue in self.generic_url_return(url, returnvalue)

class SimpleTest(GenericTest):
    def test_simple_connection():
        self.generic_url_return_startswith(SERVER+'/version',
                                           b'PS1-CRAPI:')

class Test_request(GenericTest):
    def test_invalid_request(self):
        self.generic_url_return_equal(SERVER+'/request',
                                b'ERR_INVALID_REQUEST')

    def test_unknown_machine(self):
        self.generic_url_return_equal(
            SERVER+'/request?machine=TESTNOTEXISTING&user=TESTNOTEXISTING',
            b'ERR_MACHINE_NOT_REGISTERED')

    def test_unknown_user(self):
        self.generic_url_return_equal(
            SERVER+'/request?machine=TESTMACHINE&user=TESTNOTEXISTING',
            b'ERR_USER_NOT_REGISTERED')

    def test_authorized_user(self):
        self.generic_url_return_equal(
            SERVER+'/request?machine=TESTMACHINE&user=TESTUSER',
            b'TRUE')

    def test_notauthorized_user(self):
        self.generic_url_return_equal(
            SERVER+'/request?machine=TESTMACHINE&user=TESTUSERTOBEAUTH',
            b'FALSE')

class Test_authorize(GenericTest):
    def test_auth_unauthorize_user(self):
        # Try to authorize the test user
        self.generic_url_return_equal(
            SERVER+'/authorize?machine=TESTMACHINE&auth=TESTAUTH&user=TESTUSERTOBEAUTH',
            b'TRUE')

        # Check if it is authorized
        self.generic_url_return_equal(
            SERVER+'/request?machine=TESTMACHINE&user=TESTUSERTOBEAUTH',
            b'TRUE')

        # Try to unauthorize the test user
        self.generic_url_return_equal(
            SERVER+'/unauthorize?machine=TESTMACHINE&auth=TESTAUTH&user=TESTUSERTOBEAUTH',
            b'TRUE')

        # Check if it is unauthorized
        self.generic_url_return_equal(
            SERVER+'/request?machine=TESTMACHINE&user=TESTUSERTOBEAUTH',
            b'FALSE')
