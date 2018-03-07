#app/tests/test_auth.py
import unittest
import json
import app
#authentication testcases
class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data = {'username':'monu', 'email':'fra@mail.com', 'password':'test123'}
        self.data_2 = {'username':'tito', 'email':'lawi@mail.com', 'password':'test123'}
        

    def test_user_registration(self):
        """Test user can register for account."""
        responce = self.app.post('/v1/user/auth/register', data=self.data)
        result = json.loads(responce.data.decode())
        self.assertEqual(responce.status_code, 201)
        self.assertEqual(
            result['message'], 'User {} was created'. format(self.data['username']))

    def test_user_already_registered(self):
         """Test user can only register once. """     
        response = self.app.post('/v1/user/auth/register', data=self.data_2)
        self.assertEqual(response.status_code, 201)
        second_response = self.app.post('/v1/user/auth/register', data=self.data_2)
        self.assertEqual(second_response.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_response.data.decode())
        self.assertEqual(result['message'], 'User {} was created'.format(self.data_2['username']))

    def test_user_login(self):
        """Test registered user can login."""
        responce = self.app.post('v1/user/auth/register', data=self.data)
        self.assertEqual(responce.status_code, 201)
        login_result = self.app.post('/v1/user/auth/login', data=self.data)
        # get the results in json format
        result = json.loads(login_result.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], 'Logged in as {}'.format(self.data['username']))
        # Assert that the status code is equal to 200
        self.assertEqual(login_result.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user(self):
        """Test non register user cannot login"""
        non_user = {
            'username':'non',
            'password':'not-applicable'
        }
        responce = self.app.post('/v1/user/auth/login', data=non_user)
        # get the result in json
        result = json.loads(res.data.decode())

        # assert that this response must contain an error message 
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid username or password, Please try again")
