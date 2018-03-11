#app/tests/test_auth.py
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

        # #self.data_business2 = {
        #             "business_name": "Swiftnet",
        #             "industry": "Netwrking",
        #             "location": "Kisumu",
        #             "business_email": "info@swiftnet.com",
        #             "about": "All you need for networking!"}

    def test_business_registration(self):
        """Test business registration."""
        response = self.app.post('/app/v1/business/registration', data=self.data_business)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], '{} successfully created'. format(self.data_business['business_name']))
    
    def test_view_all_business(self):
        """Test all registered business."""
        response = self.app.get('/app/v1/business/businesses', data=self.data_business)
        self.assertEqual(response.status_code, 200)

