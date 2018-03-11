#app/__init__.py
#Flask class from flask module
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from app import models, routes, business

api.add_resource(routes.UserRegistration, '/app/v1/user/auth/register')
api.add_resource(routes.UserLogin, '/app/v1/user/auth/login')
api.add_resource(routes.UserLogout, '/app/v1/user/auth/logout')
api.add_resource(routes.UserResetPassword, '/app/v1/user/auth/resetPassword')
api.add_resource(routes.BusinessRegistration, '/app/v1/business/registration')
api.add_resource(routes.AllBusiness,'/app/v1/business/businesses')
api.add_resource(routes.GetBusinessById, '/app/v1/business/<int:business_id>')

