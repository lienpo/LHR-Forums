from typing import List

from common import database
from models.post import Post

from common.connections import create_connection
from common.connection_poll import get_connection
import common.database

class Topic:
    def __init__(self, TITLE: str, CONTENT: str, OWNER: str,  _ID: int = None):
        self.id = _ID
        self.title = TITLE
        self.content = CONTENT
        self.owner = OWNER

    def __repr__(self):
        return f"Topic({self.title!r}, {self.content!r}, {self.owner!r}, {self.id!r})"

    def save(self):
        with get_connection() as connection:
            new_topic_id = database.create_topic(connection, self.title, self.content, self.owner)
            self.id = new_topic_id

    @classmethod
    def get_by_name(cls, topic_name: str) -> database.Topic:
        with get_connection() as connection:
            topic = database.get_topic_by_name(connection, topic_name)
            return topic

    def all_topics(self) -> List["Topic"]:
        with get_connection() as connection:
            topics = database.select_all_topics(connection)
            return [Topic(topic[1], topic[2], topic[3], topic[0]) for topic in topics]

    def posts(self, topic_name: str) -> List[Post]:
        with get_connection() as connection:
            posts = database.posts_in_topic(connection, topic_name)
            return [Post(post[1], post[2], post[3], post[0]) for post in posts]

    def latest_post_in_topic(self) -> database.Post:
        with get_connection() as connection:
            post = database.latest_post_in_topic(connection, self.id)
            return post

    def add_post(self, post_text: str, username: str):
        Post(post_text, self.title, username).save()


    @classmethod
    def edit_topic(cls, original_title: str, new_title: str, content: str):
        with get_connection() as connection:
            database.edit_topic(connection, new_title, original_title, content)