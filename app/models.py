
class User():
    """ User Class"""
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def resetPassword(self, reset_password):
        self.password = reset_password

class Business():
    """Business Class"""
    
    def __init__(self, business_id, business_name, industry, location, business_email,
                about, user_id, review_id):
        self.business_id = business_id
        self.business_email = business_name
        self.industry = industry
        self.location = location
        self.business_email = business_email
        self.about = about
        self.user_id = user_id
        self.review_id = review_id
        