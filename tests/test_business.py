import unittest
import json
from app import create_app


class BusinessTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined username, email and password
        self.business_data = {
            'business_name': 'Hitech',
            'business_category': 'Tech',
            'business_location': 'Mombasa, Kenya',
            'business_email': 'info@hitech.ke',
            'about': 'A well developed tech organization with all solutions you need'
        }

        self.business_put_data = {
            'business_name': 'Pytec',
            'business_category': 'Tech',
            'business_location': 'Nairobi, Kenya',
            'business_email': 'info@pytech.ke',
            'about': 'A well developed organization with all solutions you need'
        }

        self.user_data_buss = {
              'username': 'carroy',
              'user_email': 'carroy@example.com',
              'password': 'carroy_12356'
          }

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_buss)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_buss)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().post('/api/v1/business/registration', headers=dict(Authorization='Bearer ' + access_token), data=self.business_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'],"Your business was succesfully created.")
        self.assertEqual(res.status_code, 201)
    
    def test_view_all_business(self):
        """Test get all registered business."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_buss)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_buss)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().post('/api/v1/business/registration', headers=dict(Authorization='Bearer ' + access_token), data=self.business_put_data)
        res = self.client().post('/api/v1/business/registration', headers=dict(Authorization='Bearer ' + access_token), data=self.business_data)
        res = self.client().get('/api/v1/business/businesses', headers=dict(Authorization='Bearer ' + access_token))
        # get the results returned in json format
        self.assertEqual(res.status_code, 200)

    def test_view_business_by_id(self):
        """Test get a single business by id."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_buss)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_buss)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().post('/api/v1/business/registration',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.business_data)
        res = self.client().get('/api/v1/business/1',
                                 headers=dict(Authorization='Bearer ' + access_token))
        # get the results returned in json format
        self.assertEqual(res.status_code, 200)

    def test_delete_business_by_id(self):
        """Test delete a single business by id."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_buss)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_buss)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().post('/api/v1/business/registration',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.business_put_data)
        res = self.client().post('/api/v1/business/registration',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.business_data)
        res = self.client().delete('/api/v1/business/2',
                                 headers=dict(Authorization='Bearer ' + access_token))
        # get the results returned in json format
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['message'], 'Business successfully deleted!')

    def test_update_business(self):
        """Test update business. """
        res = self.client().post('/api/v1/auth/register', data=self.user_data_buss)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_buss)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().put('/api/v1/business/1',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.business_put_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        #get the result in json
        # status code 200
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result['message'], "Business succcessfully updated!")

if __name__ == '__main__':
    unittest.main()
