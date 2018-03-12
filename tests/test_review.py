#app/tests/test_business.py
import unittest
import json
import app

#business testcases


class ReviewTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.data_review = {
            "review": "Best in town",
            "business_id": 1}


    def test_business_review(self):
        """Test business review."""
        response = self.app.post('/app/v1/business/1/reviews', data=self.data_review)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['Business Review'], '{}'. format(self.data_review['review']))
