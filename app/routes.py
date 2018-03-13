#app/routes.py
from flask import Flask, Response
from app import app
from app.models.user import User
from app.models.business import Business
from app.models.review import Review
import json
from flask_restful import Resource,reqparse
from flasgger import swag_from

#parser for creating account
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

#parser for logging in and out
parser_login = reqparse.RequestParser()
parser_login.add_argument('username', help = 'This field cannot be blank', required = True)
parser_login.add_argument('password', help = 'This field cannot be blank', required = True)

#parser for reseting password
parser_reset = reqparse.RequestParser()
parser_reset.add_argument('username', help = 'This field cannot be blank', required = True)
parser_reset.add_argument('password', help = 'This field cannot be blank', required = True)
parser_reset.add_argument('new_pass', help = 'This field cannot be blank', required = True)

#parser for creating business
parser_business = reqparse.RequestParser()
parser_business.add_argument('business_name', help = 'This field cannot be blank', required = True)
parser_business.add_argument('industry', help = 'This field cannot be blank', required = True)
parser_business.add_argument('location', help = 'This field cannot be blank', required = True)
parser_business.add_argument('email', help = 'This field cannot be blank', required = True)
parser_business.add_argument('about', help='This field cannot be blank', required=True)

#parser for creating business review
parser_review = reqparse.RequestParser()
parser_review.add_argument('review', help = 'This field cannot be blank', required = True)
parser_review.add_argument('business_id', help = 'This field cannot be blank', required = True)
users = []
businesses = []
reviews = []


class UserRegistration(Resource):
    @swag_from('doc/post_user.yml')
    def post(self):
        data = parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']
        
        user_name = [x.username for x in users]
        
        if username in user_name:
            response = {'message': 'Username {} already taken'.format(data['username'])}
            return response, 202
        else:
            try:
                new_user = User(
                    username=username,
                    email=email,
                    password=password
                )
                users.append(new_user)
                response = {'message':'User {} created successfully'. format(data['username'])}
                return response, 201

            except:
                return {'message':'Something went wrong'}, 500


class UserLogin(Resource):
    @swag_from('doc/login_user.yml')
    def post(self):
        data = parser_login.parse_args()
        username = data['username']    
        password = data['password']

        current_user = [x.username for x in users]
        current_password = [x.password for x in users]

        
        if username in current_user and password in current_password:
            response = {'message': 'User {} logged in successfully' .format(data['username'])}, 202
            return response
        else:
            response = {'message': "Invalid username or password, Please try again"}
            return response, 401

class UserLogout(Resource):
    @swag_from('doc/logout_user.yml')
    def post(self):
        data = parser_login.parse_args()
        username = data['username']
        password = data['password']
        current_user = [user for user in users if user.username == username]
        if current_user[0].password == password:
            response = {'message': 'Logged out successfully'}
            return response, 200
        else:
            return {'message': 'Something went wrong'}, 500

class UserResetPassword(Resource):
    @swag_from('doc/reset_password.yml')
    def post(self):
        data = parser_reset.parse_args()
        username = data['username']
        password = data['password']
        new_pass = data['new_pass']
        current_user = [user for user in users if user.username == username]
        if current_user[0].password == password:
            current_user[0].resetPassword(new_pass)
            response = {'message':"Password reset successfully"}
            return response, 200
        else:
            return {'message':'User not found'}, 400
        
            
            
class BusinessRegistration(Resource):
    @swag_from('doc/register_business.yml')
    def post(self):
        data = parser_business.parse_args()
        business_name = data['business_name']
        industry = data['industry']
        location = data['location']
        email = data['email']
        about = data['about']
        #List all available business        
        business_list = [x.business_name for x in businesses]
        #check if business name is available in the business list
        if business_name in business_list:           
            response = {'message': '{} exists try another name'.format(data['business_name'])}
            return response, 202
        else:
            new_business = Business(
                business_name,
                industry,
                location,
                email,
                about
            )
            #create and append new business in businesses
            businesses.append(new_business)
            response = {'message': '{} successfully created'. format(data['business_name'])}          
            return response, 201

    
#get all available business list
class AllBusiness(Resource):
    """View all avilable businesses"""
    @swag_from('doc/view_all_business.yml')
    def get(self):
        mybusinesses = [{x.business_id : [x.business_name, x.industry, x.location, x.email] for x in businesses}]
        return {"Business Catalog" : mybusinesses}, 200

class GetBusinessById(Resource):
    """view business by business id"""
    @swag_from('doc/get_businesses.yml')
    def get(self, business_id):
        myBusiness = [x for x in businesses if x.business_id == business_id]
        if myBusiness:
            myBusiness = myBusiness[0]
            return {"Business Name": myBusiness.business_name, "Industry": myBusiness.industry, "Location": myBusiness.location, "Business email": myBusiness.email}, 200

        else:
            return {'message' :'Business not found'}, 404

    @swag_from('doc/delete_businesses.yml')
    def delete(self, business_id):
        myBusiness = [x for x in businesses if x.business_id == business_id]
        if myBusiness:
            del myBusiness[0]
            return {'message':'Business successfully deleted!'}, 200
        else:
            return {'message': 'Business not found'}, 404

    @swag_from('doc/update_business.yml')
    def put(self, business_id):
        data = parser_business.parse_args()
        newname = data['business_name']
        newindustry = data['industry']
        newlocation = data['location']
        newemail = data['email']
        newabout = data['about']

        myBusiness = [x for x in businesses if x.business_id == business_id]
        if myBusiness:
            myBusiness[0].update_business(newname, newindustry, newlocation, newemail, newabout)
            return {"message": "Business succcessfully updated!", }, 201
class BusinessReview(Resource):
    @swag_from('doc/post_review_business.yml')
    def post(self, business_id):
        data = parser_review.parse_args()
        review = data['review']
        business_id = data['business_id']
        business_review = [x.review for x in reviews]
        if review in business_review:
            return {'message': 'You have already reviewed the business'}
        else:
            new_review = Review(review, business_id)
            reviews.append(new_review)
            response = {"Business Review": "{}".format(data['review'])}
            return response, 201
    @swag_from('doc/get_business_review.yml')       
    def get(self, business_id):
        myReviews = [{x.review_id:[x.review] for x in reviews}]
        return {'Reviews': myReviews}, 200
