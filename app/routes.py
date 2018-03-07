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
        username = data['username'],
        email = data['email'],
        password = data['password']
        
        user_nam = [User.username for User in users]
        print(user_nam)
        print(user_nam)
        
        if username in user_nam:
                response = {'message': 'User {} was created'.format(data['username'])}
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

            

