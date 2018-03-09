#app/routes.py
from flask import Flask, Response
from app import app
from app.models import User, Business
import json
from flask_restful import Resource,reqparse

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
parser_business.add_argument('business_id', help = 'This field cannot be blank', required = True)
parser_business.add_argument('business_name', help = 'This field cannot be blank', required = True)
parser_business.add_argument('industry', help = 'This field cannot be blank', required = True)
parser_business.add_argument('location', help = 'This field cannot be blank', required = True)
parser_business.add_argument('business_email', help = 'This field cannot be blank', required = True)
parser_business.add_argument('about', help='This field cannot be blank', required=True)
parser_business.add_argument('user_id', help='This field cannot be blank', required=True)
parser_business.add_argument('review_id', help = 'This field cannot be blank', required = True)


users = []
businesses = []
class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']
        
        user_name = [User.username for User in users]
        
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
    def post(self):
        data = parser_login.parse_args()
        username = data['username']    
        password = data['password']

        current_user = [User.username for User in users]
        current_password = [User.password for User in users]

        
        if username in current_user and password in current_password:
            response = {'message': 'User {} logged in successfully' .format(data['username'])}
            return response
        else:
            response = {'message': "Invalid username or password, Please try again"}
            return response, 401

class UserLogout(Resource):
    def post(self):
        data = parser_login.parse_args()
        username = data['username']
        password = data['password']
        current_user = [user for user in users if user.username == username]
        if current_user[0].password == password:
            response = {'message': 'Logged out successfully'}
            return response, 200

class UserResetPassword(Resource):
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
        
            
            
class BusinessRegistration(Resource):
    def post(self):
        data = parser_business.parse_args()
        business_id = data['business_id']
        business_name = data['business_name']
        industry = data['industry']
        location = data['location']
        business_email = data['business_email']
        about = data['about']
        user_id = data['user_id']
        review_id = data['review_id']
        
        business_list = [Business.business_name for Business in businesses]  
        if business_name in business_list:
            
            response = {'message': '{} exists'.format(data['business_name'])}
            return response, 202
        else:
            try:
                new_business = Business(
                    business_id = business_id,
                    business_name = business_name,
                    industry = industry,
                    location = location,
                    business_email = business_email,
                    about = about,
                    user_id = user_id,
                    review_id = review_id
                )
                businesses.append(new_business)
                response = {'message': '{} successfully created'. format(data['business_name'])}
                return response, 201

            except:
                return {'message':'Something went wrong'}, 500
