from typing import Union, List

from project.dao import MovieDAO, GenreDAO, UserDAO, DirectorDAO
from project.exceptions import ItemNotFound


class BaseService:
    def __init__(self, dao: Union[MovieDAO, GenreDAO, DirectorDAO, UserDAO]) -> None:
        self.dao = dao

    def get_one(self, uid: int) -> object:
        item = self.dao.get_one(uid)
        if not item:
            raise ItemNotFound
        return item

    def get_all(self, page: str = None) -> List[object]:

        items = self.dao.get_all(page, sort=False)
        if not items:
            raise ItemNotFound
        return items
