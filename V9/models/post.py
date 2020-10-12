from typing import List
import datetime
from flask_sqlalchemy import SQLAlchemy

import common.Database.post as Database
from models.user import User
from models.reply import Reply
from common.connection_pool import get_connection


class Post:
    def __init__(self, CONTENT: str, TOPIC_ID: int, CREATOR_NAME: str,  _ID: int = None, _ORIGIN: datetime = None, REPLY_COUNT: int = 0):
        self.content = CONTENT
        self.topic_id = TOPIC_ID
        self.reply_count = REPLY_COUNT
        self.creator_name = CREATOR_NAME
        self.origin = datetime.datetime.now() if _ORIGIN is None else _ORIGIN
        self.id = _ID

    def __repr__(self) -> str:
        return f"Post({self.id!r}, {self.origin!r}, {self.reply_count!r}," \
               f" {self.content!r}, {self.topic_id!r}, {self.creator_name})"

    def save(self):
        with get_connection() as connection:
            new_post_id = Database.create_post(connection, self.origin, self.reply_count, self.content, self.topic_id, self.creator_name)
            self.id = new_post_id

    def reply_count(self) -> int:
        with get_connection() as connection:
            count = Database.reply_count(connection, self.id)
            return count

    # Post tuple ---  Post = Tuple[int, datetime, bool, int, str, int, int]
    # Classmethod tuple  ---  str, int, int, int, datetime
    @classmethod
    def all(cls) -> List["Post"]:
        with get_connection() as connection:
            posts = Database.get_posts(connection)
            return [cls(post[3], post[4], post[5], post[0], post[1], post[2]) for post in posts]

    @classmethod
    def get_by_id(cls, post_id) -> "Post":
        with get_connection() as connection:
            post = Database.get_posts_by_id(connection, post_id)
            return cls(post[3], post[4], post[5], post[0], post[1], post[2])

    @classmethod
    def all_in_topic(cls, topic_id) -> List["Post"]:
        with get_connection() as connection:
            posts = Database.get_posts_in_topic(connection, topic_id)
            return [cls(post[3], post[4], post[5], post[0], post[1], post[2]) for post in posts]

    @classmethod
    def all_by_user(cls, user_id) -> List["Post"]:
        with get_connection() as connection:
            posts = Database.get_posts_by_user(connection, user_id)
            return [cls(post[3], post[4], post[5], post[0], post[1], post[2]) for post in posts]

    @classmethod
    def ten_newest(cls) -> List["Post"]:
        with get_connection() as connection:
            posts = Database.ten_newest_posts(connection)
            return [cls(post[3], post[4], post[5], post[0], post[1], post[2]) for post in posts]

    @staticmethod
    def edit_post(new_content, post_id):
        with get_connection() as connection:
            Database.update_post(connection, new_content, post_id)

    @staticmethod
    def delete_post(post_id):
        with get_connection() as connection:
            Database.delete_post(connection, post_id)


    @classmethod
    def replying_users(cls, post_id) -> List["User"]:
        with get_connection() as connection:
            all_creator_names = Database.users_that_replied_to_post(connection, post_id)
            users = []
            for name in all_creator_names:
                users.append(User.get_by_username(name))
            return users

    @classmethod
    def has_replies(cls, post_id) -> bool:
        with get_connection() as connection:
            does_it = Database.has_replies(connection, post_id)
            return does_it

    @classmethod
    def all_replies(cls, post_id) -> List["Reply"]:
        with get_connection() as connection:
            replies = Database.post_replies(connection, post_id)
            return replies

    @classmethod
    def amt_of_replies(cls, post_id) -> int:
        with get_connection() as connection:
            count = Database.reply_count(connection, post_id)
            return count

