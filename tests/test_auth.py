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
        self.data_3 = {'username':'ribo', 'email':'riwi@mail.com', 'password':'testtest'}
        self.data_4 = {'username':'kiwi', 'email':'kiwi@mail.com', 'password':'sart'}
        self.data_5 = {'username':'coso', 'email':'coso@mail.com', 'password':'small12'}
        self.data_6 = {'username':'colo', 'email':'colo@mail.com', 'password':'jamu'}
        self.data_7 = {'username': 'colo', 'email': 'colo@mail.com', 'password': 'jamu', 'new_pass': 'ioki'}
        

    def test_user_registration(self):
        """Test user can register for account."""
        responce = self.app.post('/app/v1/user/auth/register', data=self.data_2)
        result = json.loads(responce.data.decode())
        self.assertEqual(responce.status_code, 201)
        self.assertEqual(result['message'], 'User {} was created'. format(self.data_2['username']))

    def test_user_already_registered(self):
        """Test user can only register once. """     
        response = self.app.post('/app/v1/user/auth/register', data=self.data)
        self.assertEqual(response.status_code, 201)
        second_response = self.app.post('/app/v1/user/auth/register', data=self.data)
        self.assertEqual(second_response.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_response.data.decode())
        self.assertEqual(result['message'], 'User {} is available'.format(self.data['username']))

    def test_user_login(self):
        """Test registered user can login."""
        login_result = self.app.post('/app/v1/user/auth/login', data=self.data)
        # get the results in json format
        result = json.loads(login_result.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], 'User {} logged in successfully'.format(self.data['username']))
        # Assert that the status code is equal to 200
        self.assertEqual(login_result.status_code, 200)
        #self.assertTrue(result['access_token'])

    def test_non_registered_user(self):
        response = self.app.post('/app/v1/user/auth/register', data=self.data_3)
        self.assertEqual(response.status_code, 201)
        """Test non register user cannot login"""
        non_user = {
            'username':'non',
            'password':'not-applicable'
        }
        response = self.app.post('/app/v1/user/auth/login', data=non_user)
        # get the result in json
        result = json.loads(response.data.decode())

        # assert that this response must contain an error message 
        # and an error status code 401(Unauthorized)
        self.assertEqual(response.status_code, 401)       
        self.assertEqual(result['message'], "Invalid username or password, Please try again")

    
    def test_user_wrong_password(self):
        """Test registered user cannot login with a wrong password"""
        response = self.app.post('/app/v1/user/auth/register', data=self.data_4)
        self.assertEqual(response.status_code, 201)

        user_no_pass = {
            'username': 'kiwi',
            'email': 'kiwi@mail.com',
            'password': 'not-applicable'
        }

        response = self.app.post('/app/v1/user/auth/login', data=user_no_pass)
        # get the result in json
        result = json.loads(response.data.decode())

        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result['message'], "Invalid username or password, Please try again")


    def test_user_logout(self):
        """Test user can logout the account. """
        response = self.app.post('/app/v1/user/auth/register', data=self.data_5)
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/app/v1/user/auth/login', data=self.data_5)
        response = self.app.post('/app/v1/user/auth/logout', data=self.data_5)
        # get the result in json
        result = json.loads(response.data.decode())
        # and an error status code 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], "Logged out successfully")

    def test_user_reset_password(self):
        """Test user can reset password. """
        response = self.app.post('/app/v1/user/auth/register', data=self.data_6)
        self.assertEqual(response.status_code, 201)
        response = self.app.post('/app/v1/user/auth/login', data=self.data_6)
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/app/v1/user/auth/resetPassword', data=self.data_7)
        #get the result in json
        result = json.loads(response.data.decode())
        # and an error status code 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], "Password reset successfully")



