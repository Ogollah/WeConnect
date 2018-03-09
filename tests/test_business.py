#app/tests/test_auth.py
import unittest
import json
import app

#business testcases
class BusinessTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data_business = {"business_id": "1",
                              "business_name": "PineTech",
                              "industry": "Software",
                              "location": "Msa",
                              "business_email": "info@pinetech.com",
                              "about": "Super cool!",
                              "user_id": "1",
                              "review_id": "1"}

    def test_business_registration(self):
        """Test business registration."""
        responce = self.app.post('/app/v1/business/registration', data=self.data_business)
        result = json.loads(responce.data.decode())
        self.assertEqual(responce.status_code, 201)
        self.assertEqual(result['message'], '{} successfully created'. format(self.data_business['business_name']))
     