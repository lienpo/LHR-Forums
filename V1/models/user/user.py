from models.post import Post
from models.topic import Topic
import common.database as database
from common.connection_poll import get_connection
from common.utils import Utils
import models.user.errors as UserErrors

class User:
    def __init__(self, USERNAME: str, EMAIL: str, PASSWORD: str, ID: int = None):
        self.id = ID
        self.username = USERNAME
        self.email = EMAIL
        self.password = PASSWORD

    def __repr__(self):
        return f"User({self.username!r}, {self.email!r}, {self.password!r}, {self.id!r})"

    def save(self):
        with get_connection() as connection:
            new_user_id = database.create_user(connection, self.username, self.email, self.password)
            self.id = new_user_id

    @classmethod
    def user_already_exists(cls, username: str, password: str) -> bool:
        if database.does_user_exist(username, password):
            return True
        else:
            return False

    @classmethod
    def register_user(cls, username: str, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The e-mail does not have the right format.')

        if cls.user_already_exists(username, password):
            raise UserErrors.UserAlreadyRegistered('This username already exists. Please choose a different one.')
        else:
            User(username, email, password).save()

        return True