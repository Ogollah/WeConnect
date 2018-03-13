class Business:
    class_counter = 1

    def __init__(self, business_name, industry, location, email, about):
        self.business_name = business_name
        self.industry = industry
        self.location = location
        self.email = email
        self.about = about
        self.business_id = Business.class_counter
        Business.class_counter += 1

    def update_business(self, newname, newindustry, newlocation,newemail, newabout):
        self.business_name = newname
        self.industry = newindustry
        self.location = newlocation
        self.email = newemail
        self.about = newabout
