from typing import List
import datetime

import common.database.topics as Database
from common.connection_pool import get_connection
from models.post import Post
from models.user import User

class Topic:
    def __init__(self, TITLE: str, CONTENT: str, CREATOR_NAME: str, SECTION_ID: int, _ID: int = None, _ORIGIN: datetime = None):
        self.title = TITLE
        self.content = CONTENT
        self.creator_name = CREATOR_NAME
        self.section_id = SECTION_ID
        self.origin = datetime.datetime.now() if _ORIGIN is None else _ORIGIN
        self.id = _ID

    def __repr__(self) -> str:
        return f"Topic({self.id!r}, {self.origin!r}, {self.title!r}, {self.content!r}, {self.creator_name!r}, {self.section_id} )"

    def save(self):
        with get_connection() as connection:
            new_topic_id = Database.create_topic(connection, self.origin, self.title, self.content, self.creator_name, self.section_id)
            self.id = new_topic_id

    # Topic tuple  ---  int, datetime, str, str, int, int
    # Classmethod tuple  ---  str, str, int, int, datetime
    @classmethod
    def all(cls) -> List["Topic"]:
        with get_connection() as connection:
            topics = Database.get_topics(connection)
            return [cls(topic[2], topic[3], topic[4], topic[5], topic[0], topic[1]) for topic in topics]

    @classmethod
    def get_by_id(cls, topic_id) -> "Topic":
        with get_connection() as connection:
            topic = Database.get_topic_by_id(connection, topic_id)
            return cls(topic[2], topic[3], topic[4], topic[5], topic[0], topic[1])

    @classmethod
    def give_all_topicnames(cls) -> List[str]:
        with get_connection() as connection:
            topics = Database.get_topics(connection)
            return [(topic[2]) for topic in topics]

    @classmethod
    def all_by_user(cls, user_id) -> List["Topic"]:
        with get_connection() as connection:
            topics = Database.get_topics_by_user(connection, user_id)
            return [cls(topic[2], topic[3], topic[4], topic[5], topic[0], topic[1]) for topic in topics]

    @classmethod
    def all_in_section(cls, section_id) -> List["Topic"]:
        with get_connection() as connection:
            topics = Database.get_topics_in_section(connection, section_id)
            return [cls(topic[2], topic[3], topic[4], topic[5], topic[0], topic[1]) for topic in topics]

    @classmethod
    def get_by_title(cls, title) -> "Topic":
        with get_connection() as connection:
            topic = Database.get_topic_by_title(connection, title)
            return cls(topic[2], topic[3], topic[4], topic[5], topic[0], topic[1])

    @classmethod
    def containing_topic(cls, topic_id) -> "Topic":
        topic = cls.get_by_id(topic_id)
        return topic

    @staticmethod
    def does_topic_exist(title) -> bool:
        with get_connection() as connection:
            answer = Database.check_for_title(connection, title)
            return answer

    @staticmethod
    def edit_topic(new_title, new_content, topic_id):
        with get_connection() as connection:
            Database.update_topic(connection, new_title, new_content, topic_id)

    @staticmethod
    def delete_topic(topic_id):
        with get_connection() as connection:
            Database.delete_topic(connection, topic_id)

    @staticmethod
    def users_in_topic(topic_id) -> List["User"]:
        posts_in_topic = Post.all_in_topic(topic_id)
        users = []
        for post in posts_in_topic:
            user = User.get_by_username(post.creator_name)
            users.append(user)
        return [user for user in users]

    @staticmethod
    def topic_of_post(post_id) -> "Topic":
        post = Post.get_by_id(post_id)
        for topic in Topic.all():
            if topic.id == post.topic_id:
                return topic