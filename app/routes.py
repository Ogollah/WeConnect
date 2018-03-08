#app/routes.py
from flask import Flask, request, Response, jsonify, make_response
from app import app
from app.models import User
import json
from flask_restful import Resource,reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


users = []
class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']
        
        user_nam = [User.username for User in users]
        
        if username in user_nam:
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
        data = parser.parse_args()
        username = data['username']
        email = data['email']
        password = data['password']

        current_user = [User.username for User in users]
        current_password = [User.password for User in users]
        current_email = [User.email for User in users]
        print(current_user)
        print(current_email)
        print(current_password)
        if username in current_user and password in current_password:
            print(username, password)
            response = {'message': 'User {} logged in successfully' .format(data['username'])}
            return response
        else:
            response = {'message': "Invalid username or password, Please try again"}
            return response, 401


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'Logged out successfully'}
        

            

