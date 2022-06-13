from flask import request
from flask_restx import Resource, Namespace, fields, abort
from marshmallow import ValidationError
from werkzeug.exceptions import MethodNotAllowed

from project.dao.models import UserSchema
from project.container import user_service, auth_service
from project.exceptions import ItemNotFound, IncorrectPassword

user_ns = Namespace('user', description="Views for users")
user_schema = UserSchema()

# Define api model for documentation
user_model = user_ns.model('User', {
    'id': fields.Integer(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'name': fields.String(required=True),
    'surname': fields.String(),
    'favorite_genre_id': fields.Integer()
})


@user_ns.route('/')
class UserView(Resource):
    @auth_service.auth_required
    @user_ns.doc(description='Get user by id')
    @user_ns.response(200, 'Success', user_model)
    @user_ns.response(404, 'Not Found')
    def get(self):
        try:
            # Get token
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_token(token)

            # Get and update data
            user = user_service.get_by_email(email)
            user_dict = user_schema.dump(user)
            return user_dict, 200
        except ItemNotFound:
            abort(404, 'User not found')

    @auth_service.auth_required
    @user_ns.doc(description='Get user by id')
    @user_ns.response(200, 'User updated', user_model)
    @user_ns.response(405, 'Method not allowed')
    @user_ns.response(404, 'Not Found')
    @user_ns.response(404, 'Wrong fields passed')
    def patch(self):
        try:
            # Get token
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_token(token)

            # Get and update data
            updated_data = user_schema.dump(request.json)
            user_service.update_info(updated_data, email)
            return "", 200
        except MethodNotAllowed:
            abort(405, "You're not allowed to change the data passed")
        except ItemNotFound:
            abort(404, 'User not found')
        except ValidationError:
            abort(400, 'Wrong fields passed')


@user_ns.route('/password/')
class PasswordView(Resource):
    @auth_service.auth_required
    @user_ns.doc(description='Update user password')
    @user_ns.response(200, 'Password updated', user_model)
    @user_ns.response(404, 'Not Found')
    @user_ns.response(405, 'Method not allowed')
    def put(self):
        try:
            # Get token
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_token(token)

            # Get and update data
            passwords = request.json
            user_service.update_password(passwords, email)
            return "", 200
        except ItemNotFound:
            abort(404, 'User not found')
        except IncorrectPassword:
            abort(401, 'Password is incorrect')
        except MethodNotAllowed:
            abort(405, 'Invalid data passed')
