"""Application models."""
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from datetime import datetime, timedelta
#import config

USERS = []
BUSINESSES = []
REVIEWS = []


class User(object):
    """User model."""
    class_counter = 1

    def __init__(self):
        self.username = None
        self.user_email = None
        self.password = None
        self.user_id = User.class_counter
        User.class_counter += 1


    def set_password_hash(self, password):
        """Set password hash."""
        self.password = generate_password_hash(password)

    def check_password_hash(self, password):
        """Check password hash."""
        return check_password_hash(self.password, password)

    @staticmethod
    def get_user_by_user_id(user_id):
        """Filter user by user_id."""
        for user in USERS:
            if user.user_id == user_id:
                return user

    @staticmethod
    def get_user_by_username(username):
        """Filter user by username."""
        for user in USERS:
            if user.username == username:
                return user

    def save_user(self):
        """Save a user in USERS."""
        USERS.append(self)

    def reset_password(self, new_password):
        """
        Update/reset the user password.
        :param new_password: New User Password
        :return:
        """
        self.password = new_password

class Business(object):
    """Business class model"""
    class_counter = 1

    def __init__(self):
        """Initializes business details"""
        self.business_name = None
        self.business_location = None
        self.business_email = None
        self.business_category = None
        self.about = None
        self.business_id = Business.class_counter
        Business.class_counter += 1

    def update_business(self, new_name, new_category, new_location, new_email, new_about):
        self.business_name = new_name
        self.business_category = new_category
        self.business_location = new_location
        self.business_email = new_email
        self.about = new_about

    @staticmethod
    def get_business_by_business_name(business_name):
        """Get business by its name."""
        for business in BUSINESSES:
            if business.business_name == business_name:
                return business

    @staticmethod
    def get_busines(self):
        """Get all business."""
        return BUSINESSES

    @staticmethod
    def get_business_by_business_id(business_id):
        """Get business by its id."""
        for business in BUSINESSES:
            if business.business_id == business_id:
                return business

    @staticmethod
    def delete_business(self):
        """Delete business method."""
        BUSINESSES.remove(self)

    def save_business(self):
        """Save business in BUSINESSES list."""
        BUSINESSES.append(self)


class Review(object):
    """Business review class model"""
    class_counter = 1

    def __init__(self):
        """Initializes review details"""
        self.business_review = None
        self.review_id = Review.class_counter
        Review.class_counter += 1

    @staticmethod
    def get_review_by_id(review_id):
        """Get business by its id."""
        for review in REVIEWS:
            if review.review_id == review_id:
                return review

    @staticmethod
    def get_reviews(self):
        """Get all reviews."""
        return REVIEWS

    def save_review(self):
        """Save business in BUSINESSES list."""
        REVIEWS.append(self)
