# /app/auth/views.py

from . import auth_blueprint

import re
from flask.views import MethodView
from flask import make_response, request, jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, create_access_token
from ..models import User, Business, Review

blacklist = set()

class RegistrationView(MethodView):
    """Register new user"""

    def post(self):
        """User registration method"""
        #Check if user already exists
        user = User.get_user_by_username(username = request.data['username'])
        if not user:
            #If there is no user try to add a new user
            try:
                add_data = request.data 
                username = add_data['username']
                user_email = add_data['user_email']
                password = add_data['password']
                add_user = User()
                add_user.username = username
                add_user.user_email = user_email
                add_user.set_password_hash(password)
                add_user.save_user()

                response = {"message": "Your account was succesfully created."}
                #return a response of account creasion
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # Return a message to the user telling them that they they already exist
            response = {"message": "User with this username already exists kindly try another one!."}
            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """Logging in registred user"""

    def post(self):
        """Method for logging in a registered user"""
        username = request.data['username']
        registred_user = User.get_user_by_username(username=request.data['username'])
        if registred_user and registred_user.check_password_hash(request.data['password']):
            # Generate the access token. This will be used as the authorization header
            access_token = create_access_token(identity=username)
            response = {'message': "You have successfully logged in!.",
                            "access_token": access_token}
            return make_response(jsonify(response)), 200
        else:
            # User does not exist. Therefore, we return an error message
            response = {"message": "Invalid username or password, Please try again!"}
            return make_response(jsonify(response)), 401


class LogoutView(MethodView):
    """Logout Resource."""
    @jwt_required
    def post(self):
        """Log out a given user by blacklisting user's token
        :return
            message and status code.
        """
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        response = {"message": "You have successfully logged out"}
        return make_response(jsonify(response)), 200

class ResetPasswordView(MethodView):
    """Reset password Resource"""
    @jwt_required
    def post(self):
        """
            Reset password of a user
        :return 
            message and status code.
        """
        #username = request.data['username']
        current_user = User.get_user_by_username(username=request.data['username'])
        new_password = request.data['new_password']
        if current_user and current_user.check_password_hash(request.data['old_password']):
            current_user.reset_password(new_password)
            current_user.set_password_hash(new_password)
            response = {'message':'You have successfully reset your password.'}
            return make_response(jsonify(response)), 200
        else:
            response = {'message':'Wrong password or username'}
            return make_response(jsonify(response)), 401


class BusinessRegistrationView(MethodView):
    """Register new business."""
    @jwt_required
    def post(self):
        """abusiness registration method"""
        #Check if business already exists
        business = Business.get_business_by_business_name(business_name=request.data['business_name'])
        if not business:
            #If there is no business try to add a new business
            try:
                add_data = request.data
                business_name = add_data['business_name']
                business_email = add_data['business_email']
                business_location = add_data['business_location']
                business_category = add_data['business_category']
                about = add_data['about']
                add_business = Business()
                add_business.business_name = business_name
                add_business.business_email = business_email
                add_business.business_category = business_category
                add_business.business_location = business_location
                add_business.about = about
                add_business.save_business()

                response = {"message": "Your business was succesfully created."}
                #return a response of business creasion
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # Return a message to the user telling them that the business already exist
            response = {
                "message": "Business with this name already exists kindly try another name!"}
            return make_response(jsonify(response)), 202

class GetBusinessesView(MethodView):
    """Get Registered businesses"""
    @jwt_required
    def get(self):
        catalog = Business.get_busines(self)
        #for business in catalog:
        business = [{x.business_id: [{"Business name":x.business_name,
                                         "Category":x.business_category, "Location":x.business_location, "Email":x.business_email}] for x in catalog}]
        response = {"Catalog": business}
        return make_response(jsonify(response)), 200

class GetSingleBusinessView(MethodView):
    """ Business by id."""
    @jwt_required
    def get(self, business_id):
        """abusiness registration method"""
        #Check if business exists
        business = Business.get_business_by_business_id(business_id)
        if business:
            #result = business.business_serializer()
            response = {"Business name": business.business_name, "Category": business.business_category, "Location": business.business_location, "Email": business.business_email}
            return make_response(jsonify(response)), 200
        else:
            response = {"message":"Business was not found"}
            return make_response(jsonify(response)), 404

    @jwt_required
    def delete(self, business_id):
        """Delete business method
            return:
            Delete message successful or business not found if business not available
        """
        #Check if business exists
        business = Business.get_business_by_business_id(business_id)
        if business:
            business.delete_business(business)
            response = {"message": "Business successfully deleted!"}
            return make_response(jsonify(response)), 200
        else:
            response = {"message": "Business was not found"}
            return make_response(jsonify(response)),404

    @jwt_required
    def put(self, business_id):
        add_data = request.data
        new_name = add_data['business_name']
        new_email = add_data['business_email']
        new_location = add_data['business_location']
        new_category = add_data['business_category']
        new_about = add_data['about']
        #Check if business exists
        business = Business.get_business_by_business_id(business_id)
        if business:
            business.update_business(new_name, new_category, new_location, new_email, new_about)
            response = {"message": "Business succcessfully updated!"}
            return make_response(jsonify(response)), 201
        else:
            response = {"message": "Business was not found"}
            return make_response(jsonify(response)), 404


class BusinessReviewView(MethodView):
    @jwt_required
    def post(self, business_id):
        #Check if business exists
        business = Business.get_business_by_business_id(business_id)
        if business:
            add_data = request.data
            business_review = add_data['business_review']
            add_review = Review()
            add_review.business_review = business_review
            add_review.save_review()

            response = {
                "message": "Your review is added!"}
            #return a response of review creation
            return make_response(jsonify(response)), 201

    @jwt_required
    def get(self, business_id):
        bus_review = Review.get_reviews(self)
        #Check if business exists
        business = Business.get_business_by_business_id(business_id)
        if business:
            reviews = [{x.review_id: [x.business_review] for x in bus_review}]
            response = {business.business_name: reviews} 
            return make_response(jsonify(response)), 200

class GetSingleReviewView(MethodView):
    """ Review by id."""
    @jwt_required
    def get(self, business_id, review_id):
        """get abusiness review method"""
        #Check if business exists
        review = Review.get_review_by_id(review_id)
        business = Business.get_business_by_business_id(business_id)
        if business:

            if review:
                response = {"Business review": review.business_review}
                return make_response(jsonify(response)), 200
            else:
                response = {"message": "Review was not found"}
                return make_response(jsonify(response)), 404
   

            




            

# Define the API resource
#user
registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_password_view = ResetPasswordView.as_view('reset_password_view')

#Business
business_registration_view = BusinessRegistrationView.as_view('business_register_view')
get_business_view = GetSingleBusinessView.as_view('get_business_view')
get_businesses_view = GetBusinessesView.as_view('get_businesses_view')

#Review
add_review_view = BusinessReviewView.as_view('add_review_view')
get_single_review_view = GetSingleReviewView.as_view('get_single_review_view')

#User
# Define the rule for the registration url --->  /api/v1/auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the login url --->  /api/v1/auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST']
)

# Define the rule for the logout url --->  /api/v1/auth/logout
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/logout',
    view_func=logout_view,
    methods=['POST']
)

# Define the rule for the reset_password url --->  /api/v1/auth/reset_password
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/reset_password',
    view_func=reset_password_view,
    methods=['POST']
)

#Business
# Define the rule for the registration url --->  /api/v1/business/registration
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/business/registration',
    view_func=business_registration_view,
    methods=['POST'])

# Define the rule for the get business url --->  /api/v1/business/business
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/business/businesses',
    view_func=get_businesses_view,
    methods=['GET'])

# Define the rule for the get business url --->  /api/v1/business/<business_id>
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/business/<int:business_id>',
    view_func=get_business_view,
    methods=['GET','DELETE', 'PUT'])

#Review
# Define the rule for the registration url --->  /api/v1/business/<int:business_id>/review
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/business/<int:business_id>/review',
    view_func=add_review_view,
    methods=['POST', 'GET'])

# Define the rule for the registration url --->  /api/v1/business/<int:business_id>/<review_id>
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v1/business/<int:business_id>/<int:review_id>',
    view_func=get_single_review_view,
    methods=['GET'])

