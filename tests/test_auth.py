#app/tests/test_auth.py
import unittest
import json
import app

#authentication testcases
class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data = {'username':'manu', 'email':'manu@mail.com', 'password':'test123'}

    def test_user_registration(self):
        responce = self.app.post('/v1/user/auth/register', data=self.data)
        result = json.loads(responce.data.decode())
        self.assertEqual(responce.status_code, 201)
        self.assertEqual(
            result['message'], 'User {} was created'. format(self.data['username']))
