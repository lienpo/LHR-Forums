from typing import List
import datetime

import common.database as Database
from common.connection_pool import get_connection

class User:
    def __init__(self, USERNAME: str, EMAIL: str, PASSWORD: str, _ID: int = None, _ORIGIN: datetime = None):
        self.username = USERNAME
        self.email = EMAIL
        self.password = PASSWORD
        self.origin = datetime.datetime.now() if _ORIGIN is None else _ORIGIN
        self.id = _ID

    def __repr__(self) -> str:
        return f"User({self.id!r}, {self.origin!r}, {self.username!r}, {self.password!r})"

    def save(self):
        with get_connection() as connection:
            new_user_id = Database.create_user(connection, self.origin, self.username, self.email, self.password)
            self.id = new_user_id

    @classmethod
    def all_usernames(cls) -> List[str]:
        with get_connection() as connection:
            users = Database.get_users(connection)
            return[(user[2]) for user in users]

    @classmethod
    def all(cls) -> List["User"]:
        with get_connection() as connection:
            users = Database.get_users(connection)
            return [cls(user[2], user[3], user[4], user[0], user[1]) for user in users]


    @classmethod
    def get_by_id(cls, user_id: int) -> "User":
        with get_connection() as connection:
            user = Database.get_user_by_id(connection, user_id)
            return cls(user[2], user[3], user[4], user[0], user[1])

    @classmethod
    def get_by_username(cls, username: str) -> "User":
        with get_connection() as connection:
            user = Database.get_user_by_username(connection, username)
            return cls(user[2], user[3], user[4], user[0], user[1])

    @staticmethod
    def edit_user_profile(new_username, new_email, new_password, user_id):
        with get_connection() as connection:
            Database.update_user(connection, new_username, new_email, new_password, user_id)

    @staticmethod
    def does_user_exist(name) -> bool:
        with get_connection() as connection:
            answer = Database.check_for_username(connection, name)
            return answer

    @staticmethod
    def delete_user(user_id):
        with get_connection() as connection:
            Database.delete_user(connection, user_id)
