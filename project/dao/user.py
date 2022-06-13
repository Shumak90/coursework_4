from typing import Union

from sqlalchemy.exc import NoResultFound

from .models import User
from .base import BaseDAO


class UserDAO(BaseDAO):

    def get_by_email(self, email: str) -> Union[User, None]:

        try:
            user = self.session.query(User).filter(User.email == email).one()
            return user
        except NoResultFound:
            return None

    def create(self, data: dict) -> User:
        """Добавить пользователя в базу"""
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def update_by_email(self, data: dict, email: str) -> None:
        """Обновить пользователя data"""
        self.session.query(User).filter(User.email == email).update(data)
        self.session.commit()
