#app/__init__.py
#Flask class from flask module
import os
import inspect
from flask import Flask, redirect, Blueprint
from flasgger import Swagger
from flask_restful import Api

app = Flask(__name__)
app.config['SWAGGER'] = {
    'swagger': '2.0',
    'title': 'WeConnect API',
    'description': "This API gives users opportunity to create, review business",
    'basePath': '',
    'version': '1',
    'contact': {
                'Developer': 'stephen Ogolla',
                'Profile': 'https://github.com/Ogollah'
    },
    'license': {
    },
    'tags': [
        {
            'name': 'User',
                    'description': 'The API user'
        },
        {
            'name': 'Business',
                    'description': 'A business can be added, updated, reviewed or deleted by a user'
        },
        {
            'name': 'Review',
                    'description': 'Review can be created and viewed'
        },
    ]
}

swag = Swagger(app)
# Add Blueprint; how to construct or extend the app
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api/v1")



from app import routes
from app.models import business, review, user

api.add_resource(routes.UserRegistration, '/user/auth/register')
api.add_resource(routes.UserLogin, '/user/auth/login')
api.add_resource(routes.UserLogout, '/user/auth/logout')
api.add_resource(routes.UserResetPassword, '/user/auth/resetPassword')
api.add_resource(routes.BusinessRegistration, '/business/registration')
api.add_resource(routes.AllBusiness,'/business/businesses')
api.add_resource(routes.GetBusinessById, '/business/<int:business_id>')
api.add_resource(routes.BusinessReview , '/business/<int:business_id>/reviews')

app.register_blueprint(api_bp)

@app.route('/')
def main():
    """Redirect to api endpoints"""
    return redirect('/api/v1/')
if __name__ == '__main__':
    app.run()
