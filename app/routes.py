#app/routes.py
from flask import Flask, Response
from app import app
from app.models import User
import json
from flask_restful import Resource,reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

parser_login = reqparse.RequestParser()
parser_login.add_argument('username', help = 'This field cannot be blank', required = True)
parser_login.add_argument('password', help = 'This field cannot be blank', required = True)

parser_reset = reqparse.RequestParser()
parser_reset.add_argument('username', help = 'This field cannot be blank', required = True)
parser_reset.add_argument('password', help = 'This field cannot be blank', required = True)
parser_reset.add_argument('new_pass', help = 'This field cannot be blank', required = True)



users = []
class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']
        
        user_name = [User.username for User in users]
        
        if username in user_name:
            print(username)
            response = {'message': 'User {} is available'.format(data['username'])}
            return response, 202
        else:
            try:
                new_user = User(
                    username=username,
                    email=email,
                    password=password
                )
                users.append(new_user)
                response = {'message':'User {} was created'. format(data['username'])}
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
            
