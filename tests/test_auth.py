#app/tests/test_auth.py
import unittest
import jsonify
from app import app

#authentication testcases
class AuthTestCase(unittest.TestCase):
    
    #test user registration
    def test_user_registration(self):
        user = Users()
        response = user.register_user()
            # convert the json response to an object
        result = json.loads(response.data.decode())
            # the user should be successfully registered
        self.assertEqual(result['message'],
                             'You have registered successfully!')
        self.assertEqual(response.status_code, 201)
