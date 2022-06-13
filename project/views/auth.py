from flask import request
from flask_restx import Resource, Namespace, fields, abort
from marshmallow import ValidationError

from project.container import auth_service, user_service
from project.dao.models import UserSchema
from project.exceptions import UserAlreadyExists, ItemNotFound, IncorrectPassword, InvalidToken

auth_ns = Namespace('auth', description='Authorization and authentication')
user_schema = UserSchema()

# Определить модель API для документации
auth_model = auth_ns.model('Registration', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

tokens_model = auth_ns.model('Tokens', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
})


@auth_ns.route('/register/')
class AuthView(Resource):
    @auth_ns.doc(description='Пользователь зарегистрирован', body=auth_model)
    @auth_ns.response(201, 'Пользователь зарегистрирован')
    @auth_ns.response(400, 'Неверный запрос')
    def post(self):
        # Получить и проверить переданные учетные данные
        credentials = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        if None in credentials.values():
            abort(400, 'неправильные поля')

        # Зарегистрировать пользователя
        try:
            data = user_schema.load(credentials)
            user = user_service.create(data)
            return "", 201, {"location": f"/user/{user.id}"}
        except ValidationError:
            abort(400, 'Переданы неверные данные')
        except UserAlreadyExists:
            abort(400, 'Пользователь уже существует')


@auth_ns.route('/login/')
class AuthView(Resource):
    @auth_ns.doc(description='Get tokens', body=auth_model)
    @auth_ns.response(201, 'Токены созданы', tokens_model)
    @auth_ns.response(400, 'Неверный запрос')
    @auth_ns.response(401, 'неправильный пароль')
    @auth_ns.response(404, 'нет пользователя с таким адресом электронной почты')
    def post(self):
        # Получить и проверить переданные учетные данные
        credentials = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        if None in credentials.values():
            abort(400, 'Not valid data passed')

        try:
            tokens = auth_service.generate_tokens(credentials)
            return tokens, 201
        except ItemNotFound:
            abort(404, 'пользователь не найден')
        except IncorrectPassword:
            abort(401, 'password')

    @auth_ns.doc(description='Get new tokens')
    @auth_ns.response(201, 'ok', tokens_model)
    @auth_ns.response(401, 'Invalid refresh token')
    def put(self):
        try:
            # Check data validity
            refresh_token = request.json.get('refresh_token')
            if not refresh_token:
                abort(400, 'Not valid data passed')

            # Get tokens
            tokens = auth_service.approve_token(refresh_token)
            return tokens, 201

        except InvalidToken:
            abort(401, 'Invalid token passed')
