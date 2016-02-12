# Test suite for PS1-CRAPI
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


import tornado.httpclient
import tornado.testing
import server
from Auth.DummyAuth import DummyAuth

# The test system is based on a generic Async that creates the app
# and the test data on the fly so the server is not poluted.

class GenericTest(tornado.testing.AsyncHTTPTestCase):
    def generic_url_return(self, url, returnvalue):
        try:
            response = self.fetch(url)
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

    def get_app(self):
        """Create a server with dummy data"""
        auth = DummyAuth()
        auth.add_machine('TESTMACHINE')
        auth.add_user('TESTAUTH')
        auth.make_user_authorizer_on_machine('TESTMACHINE', 'TESTAUTH')
        auth.add_user('TESTUSER')
        auth.add_user('TESTUSERTOBEAUTH')
        auth.authorize_user('TESTMACHINE', 'TESTAUTH')
        auth.authorize_user('TESTMACHINE', 'TESTUSER')
        return server.make_app(auth)
        

class Test_version(GenericTest):
    def test_simple_version(self):
        self.generic_url_return_startswith('/version',
                                           b'PS1-CRAPI:')

class Test_request(GenericTest):
    def test_invalid_request(self):
        self.generic_url_return_equal('/request',
                                b'ERR_INVALID_REQUEST')

    def test_unknown_machine(self):
        self.generic_url_return_equal(
            '/request?machine=TESTNOTEXISTING&user=TESTNOTEXISTING',
            b'ERR_MACHINE_NOT_REGISTERED')

    def test_unknown_user(self):
        self.generic_url_return_equal(
            '/request?machine=TESTMACHINE&user=TESTNOTEXISTING',
            b'ERR_USER_NOT_REGISTERED')

    def test_authorized_user(self):
        self.generic_url_return_equal(
            '/request?machine=TESTMACHINE&user=TESTUSER',
            b'TRUE')
    def test_authorized_user_check(self):
        self.generic_url_return_equal(
            '/check?machine=TESTMACHINE&user=TESTUSER',
            b'TRUE')
        
    def test_notauthorized_user(self):
        self.generic_url_return_equal(
            '/request?machine=TESTMACHINE&user=TESTUSERTOBEAUTH',
            b'FALSE')
        
    def test_notauthorized_user_check(self):
        self.generic_url_return_equal(
            '/check?machine=TESTMACHINE&user=TESTUSERTOBEAUTH',
            b'FALSE')

class Test_authorize(GenericTest):
    def test_auth_unauthorize_user(self):
        # Try to authorize the test user
        self.generic_url_return_equal(
            '/authorize?machine=TESTMACHINE&auth=TESTAUTH&user=TESTUSERTOBEAUTH',
            b'TRUE')

        # Check if it is authorized
        self.generic_url_return_equal(
            '/request?machine=TESTMACHINE&user=TESTUSERTOBEAUTH',
            b'TRUE')

        # Try to unauthorize the test user
        self.generic_url_return_equal(
            '/unauthorize?machine=TESTMACHINE&auth=TESTAUTH&user=TESTUSERTOBEAUTH',
            b'TRUE')

        # Check if it is unauthorized
        self.generic_url_return_equal(
            '/request?machine=TESTMACHINE&user=TESTUSERTOBEAUTH',
            b'FALSE')
