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


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        new_user = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )
        
        #users = []
        try:
            User.users.append(new_user)
            response = {'message':'User {} was created'. format(data['username'])}
            return response, 201

        except:
            return {'message':'Something went wrong'}, 500
