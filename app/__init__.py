#app/__init__.py
#Flask class from flask module
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from app import models, routes


api.add_resource(routes.UserRegistration, '/v1/user/auth/register')

