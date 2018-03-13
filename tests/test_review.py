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
        response = self.app.post('/api/v1/business/1/reviews', data=self.data_review)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['Business Review'], '{}'. format(self.data_review['review']))

    def test_review_business_twice(self):
        """Test user cannot review a business twice"""
        response = self.app.post('/api/v1/business/1/reviews', data=self.data_review)
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'You have already reviewed the business')

    def test_view_all_business_review(self):
        """Test view all business review."""
        response = self.app.get('/api/v1/business/1/reviews', data=self.data_review)
        self.assertEqual(response.status_code, 200)
