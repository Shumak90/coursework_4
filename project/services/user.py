import base64
import hashlib
import hmac

from flask import current_app
from werkzeug.exceptions import MethodNotAllowed

from project.dao.models import User
from project.exceptions import UserAlreadyExists, IncorrectPassword, ItemNotFound
from project.services.base import BaseService


class UserService(BaseService):

    def get_by_email(self, email: str) -> User:

        user = self.dao.get_by_email(email)
        if not user:
            raise ItemNotFound
        return user

    def create(self, data: dict) -> User:

        # Проверить, существует ли пользователь
        user = self.dao.get_by_email(data.get('email'))
        if user:
            raise UserAlreadyExists

        # Хэш-пароль и добавление пользователя в базу данных
        data['password'] = self.hash_password(data.get('password'))
        user = self.dao.create(data)
        return user

    def update_info(self, data: dict, email: str) -> None:
        # Проверить существование пользователя
        self.get_by_email(email)
        # Проверить данные
        if 'password' not in data.keys() and 'email' not in data.keys():
            self.dao.update_by_email(data, email)
        else:
            raise MethodNotAllowed

    def update_password(self, data: dict, email: str) -> None:

        user = self.get_by_email(email)
        current_password = data.get('old_password')
        new_password = data.get('new_password')

        if None in [current_password, new_password]:
            raise MethodNotAllowed

        if not self.compare_passwords(user.password, current_password):
            raise IncorrectPassword

        data = {
            'password': self.hash_password(new_password)
        }
        self.dao.update_by_email(data, email)

    def hash_password(self, password: str) -> bytes:

        hash_digest = self.create_hash(password)
        encoded_digest = base64.b64encode(hash_digest)
        return encoded_digest

    def create_hash(self, password: str) -> bytes:

        hash_digest: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            current_app.config.get('PWD_HASH_SALT'),
            current_app.config.get('PWD_HASH_ITERATIONS')
        )
        return hash_digest

    def compare_passwords(self, password_hash: str, password_passed: str) -> bool:

        decoded_digest: bytes = base64.b64decode(password_hash)
        passed_hash: bytes = self.create_hash(password_passed)

        is_equal = hmac.compare_digest(decoded_digest, passed_hash)
        return is_equal
