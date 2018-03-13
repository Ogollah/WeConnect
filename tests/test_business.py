#app/tests/test_business.py
import unittest
import json
import app

#business testcases
class BusinessTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data_business = {
                    "business_name": "PineTech",
                    "industry": "Software",
                    "location": "Msa",
                    "email": "info@pinetech.com",
                    "about": "Super cool!"}

        self.data_business1 = {
                    "business_name": "Swiftnet",
                    "industry": "Netwrking",
                    "location": "Kisumu",
                    "email": "info@swiftnet.com",
                    "about": "All you need for networking!"}

    def test_business_registration(self):
        """Test business registration."""
        response = self.app.post('/api/v1/business/registration', data=self.data_business)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], '{} successfully created'. format(self.data_business['business_name']))
    
    def test_view_all_business(self):
        """Test all registered business."""
        response = self.app.get('/api/v1/business/businesses', data=self.data_business)
        self.assertEqual(response.status_code, 200)

    def test_view_business_by_id(self):
        """Test get a single business by id."""
        response = self.app.get('/api/v1/business/1', data=self.data_business)
        self.assertEqual(response.status_code, 200)

    def test_delete_business_by_id(self):
        """Test delete a single business by id."""
        response = self.app.delete('/api/v1/business/1', data=self.data_business)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Business successfully deleted!')

    def test_user_reset_password(self):
        """Test user can reset password. """
        response = self.app.put('/api/v1/business/1', data=self.data_business1)
        #get the result in json
        result = json.loads(response.data.decode())
        # status code 200
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], "Business succcessfully updated!")

