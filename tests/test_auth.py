import unittest
import json
from app import create_app


class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined username, email and password
        self.user_data = {
            'username': 'testexample',
            'user_email': 'test@example.com',
            'password': 'test_123'
        }
        self.user_data_2 = {
            'username': 'example',
            'user_email': 'example@example.com',
            'password': 'test_123'
        }
        self.user_data_4 = {
            'username': 'exam',
            'user_email': 'exam@example.com',
            'password': 'test_12356'
        }

        self.user_data_5 = {
            'username': 'sammy',
            'user_email': 'sammy@example.com',
            'password': 'sammy_12356'
        }

        self.user_data_6 = {
            'username': 'lookman',
            'user_email': 'looky@example.com',
            'password': 'testexample'
        }

        self.user_data_7 = {
            'username': 'kazi',
            'user_email': 'looky@example.com',
            'password': 'testexample'
        }

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'],
                         "Your account was succesfully created.")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_2)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/v1/auth/register', data=self.user_data_2)
        self.assertEqual(second_res.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User with this username already exists kindly try another one!.")

    def test_user_login(self):
        """Test registered user can login."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_4)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_4)
        # get the results in json format
        result = json.loads(login_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'],
                         "You have successfully logged in!.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'username': 'abela',
            'password': 'nopekabisa'
        }
        # send a POST request to /auth/login with the data above
        res = self.client().post('/api/v1/auth/login', data=not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid username or password, Please try again!")

    def test_user_logout(self):
        """Test registered user can logout."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_5)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_5)
        self.assertEqual(login_res.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        logout_res = self.client().post('/api/v1/auth/logout',
                                        headers=dict(Authorization='Bearer ' + access_token), data=self.user_data_5)
        # get the results in json format
        result = json.loads(logout_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result["message"], "You have successfully logged out")
        # Assert that the status code is equal to 200
        self.assertEqual(logout_res.status_code, 200)

    def test_user_can_reset_password(self):
        """Test user can change there password given correct credentials."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_6)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_6)
        self.assertEqual(login_res.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        reset_password = {
            "username": "lookman",
            "old_password": "testexample",
            "new_password": "123456"
        }
        reset_res = self.client().post('/api/v1/auth/reset_password',
                                       headers=dict(Authorization='Bearer ' + access_token), data=reset_password)
        # get the results in json format
        result = json.loads(reset_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result["message"],
                         "You have successfully reset your password.")
        # Assert that the status code is equal to 200
        self.assertEqual(reset_res.status_code, 200)

    def test_user_cannot_reset_password_with_invalid_credential(self):
        """Test user cannot change there password given incorrect credentials."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_7)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_7)
        self.assertEqual(login_res.status_code, 200)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        reset_password = {
            "username": "kazi",
            "old_password": "exampletest",
            "new_password": "123456"
        }
        reset_res = self.client().post('/api/v1/auth/reset_password',
                                       headers=dict(Authorization='Bearer ' + access_token), data=reset_password)
        # get the results in json format
        result = json.loads(reset_res.data.decode())
        # Test that the response contains a message
        self.assertEqual(result["message"],
                         "Wrong password or username")
        # Assert that the status code is equal to 401
        self.assertEqual(reset_res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
