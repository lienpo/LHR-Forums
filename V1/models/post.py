from typing import List
import datetime
import pytz

import common.database as database
from common.connection_poll import get_connection

class Post:
    def __init__(self, CONTENT: str, TOPIC: str, CREATOR: str, _ID: int = None):
        self.content = CONTENT
        self.topic = TOPIC
        self.creator = CREATOR
        self._id = _ID

    def __repr__(self) -> str:
        return f"Post({self.content!r}, {self.topic!r}, {self.creator!r}, {self._id!r})"

    def save(self):
        with get_connection() as connection:
            new_post_id = database.create_post(connection, self.content, self.topic, self.creator)
            self._id = new_post_id

    @classmethod
    def get_by_id(cls, post_id: int) -> "Post":
        with get_connection() as connection:
            post = database.get_post_by_id(connection, post_id)
            return cls(post[1], post[2], post[3], post[0])

    @classmethod
    def latest_posts(cls) -> List["Post"]:
        with get_connection() as connection:
            posts = database.newest_posts(connection)
            return [cls(post[1], post[2], post[3], post[0]) for post in posts]


    @classmethod
    def edit_post(cls, post_id, new_content) -> "Post":
        with get_connection() as connection:
            post = database.edit_post(connection, new_content, post_id)
            return cls(post[1], post[2], post[3], post[0])
