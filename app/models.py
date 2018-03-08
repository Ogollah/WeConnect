
class User():
    #users = []
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def resetPassword(self, reset_password):
        self.password = reset_password
        
        
