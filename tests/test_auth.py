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
              
        response = self.app.post('/v1/user/auth/register', data=self.data_2)
        self.assertEqual(response.status_code, 201)
        second_response = self.app.post('/v1/user/auth/register', data=self.data_2)
        self.assertEqual(second_response.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_response.data.decode())
        self.assertEqual(result['message'], 'User {} was created'.format(self.data_2['username']))
