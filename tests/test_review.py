import unittest
import json
from app import create_app


class ReviewTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined username, email and password
        self.review_data = {
            'business_review': 'This is so much like it!',
        }

        self.business_rev_data = {
            'business_name': 'Ziko',
            'business_category': 'Tech',
            'business_location': 'Nairobi, Kenya',
            'business_email': 'info@pytech.ke',
            'about': 'A well developed organization with all solutions you need'
        }

        self.user_data_rev = {
            'username': 'kasandra',
            'user_email': 'kasandra@example.com',
            'password': 'kasandra_12356'
        }

    def test_business_review(self):
        """Test user review business."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_rev)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_rev)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().post('/api/v1/business/registration',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.business_rev_data)
        res = self.client().post('/api/v1/business/1/review',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.review_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'],
                         "Your review is added!")
        self.assertEqual(res.status_code, 201)

    def test_get_business_reviews(self):
        """Test get reviews for a business."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_rev)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_rev)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().post('/api/v1/business/registration',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.business_rev_data)
        res = self.client().post('/api/v1/business/1/review',
                                         headers=dict(Authorization='Bearer ' + access_token), data=self.review_data)
        res = self.client().get('/api/v1/business/1/review',
                                headers=dict(Authorization='Bearer ' + access_token))
        # get the results returned in json format
        self.assertEqual(res.status_code, 200)

    def test_get_business_review_by_id(self):
        """Test a review for a business."""
        res = self.client().post('/api/v1/auth/register', data=self.user_data_rev)
        login_res = self.client().post('/api/v1/auth/login', data=self.user_data_rev)
        #Define header dictionary
        access_token = json.loads(login_res.data.decode())['access_token']
        res = self.client().post('/api/v1/business/registration',
                                 headers=dict(Authorization='Bearer ' + access_token), data=self.business_rev_data)
        res = self.client().post('/api/v1/business/1/review',
                                         headers=dict(Authorization='Bearer ' + access_token), data=self.review_data)
        res = self.client().get('/api/v1/business/1/1',
                                headers=dict(Authorization='Bearer ' + access_token))
        # get the results returned in json format
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
