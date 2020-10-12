from typing import List
import datetime

import common.Database.private_message as Database
from common.connection_pool import get_connection
from models.user import User


# Try to add the boolean is_new property later, but don't waste your time on it since Python wants to act retarded and punish me for adding it

class Private_Message:
    def __init__(self, SUBJECT: str, CONTENT: str,  USER_FROM: int, USER_TO: int,
                 _ID: int = None, _ORIGIN: datetime = None, IS_NEW: bool = True):

        self.id = _ID
        self.origin = datetime.datetime.now() if _ORIGIN is None else _ORIGIN
        self.is_new = IS_NEW
        self.subject = SUBJECT
        self.content = CONTENT
        self.user_from = USER_FROM
        self.user_to = USER_TO


    # int, datetime, str, str, bool, int, int
    def __repr__(self) -> str:
        return f"Private_Message({self.id!r}, {self.origin!r}, {self.is_new!r}," \
               f" {self.subject!r}, {self.content!r},  {self.user_from!r}, {self.user_to!r})"

    def save(self):
        with get_connection() as connection:
            new_private_message_id = Database.create_private_message(connection, self.origin, self.is_new,
                self.subject, self.content, self.user_from, self.user_to)
            self.id = new_private_message_id

    # Database tuple ---  int, datetime, str, str, bool, int, int
    # Classmethod tuple  ---  str, str, int, int, int, datetime
    @classmethod
    def all_my_messages(cls, user_id) -> List["Private_Message"]:
        with get_connection() as connection:
            messages = Database.get_my_mail(connection, user_id)
            return [cls(message[3], message[4], message[5], message[6], message[0], message[1], message[2])
                    for message in messages]

    @classmethod
    def all_my_senders(cls, user_id) -> List["User"]:
        messages = Private_Message.all_my_messages(user_id)
        users_from = []
        for message in messages:
            user_from_id = message.user_from
            user_from = User.get_by_id(user_from_id)
            users_from.append(user_from)
        return users_from

    @classmethod
    def get_message_by_id(cls, message_id) -> "Private_Message":
        with get_connection() as connection:
            message = Database.get_message_by_id(connection, message_id)
            return cls(message[3], message[4], message[5], message[6], message[0], message[1], message[2])

    @classmethod
    def set_as_saved(cls, message_id):
        with get_connection() as connection:
            Database.set_as_saved(connection, message_id)

    @classmethod
    def who_its_to(cls, message_id) -> "User":
        the_message = Private_Message.get_message_by_id(message_id)
        users_id = the_message.user_to
        user = User.get_by_id(users_id)
        return user

    @classmethod
    def who_its_from(cls, message_id) -> "User":
        the_message = Private_Message.get_message_by_id(message_id)
        users_id = the_message.user_from
        user = User.get_by_id(users_id)
        return user

    @classmethod
    def all_new_messages(cls, user_id) -> List["Private_Message"]:
        with get_connection() as connection:
            messages = Database.get_my_new_mail(connection, user_id)
            return [cls(message[3], message[4], message[5], message[6], message[0], message[1], message[2]) for message in messages]

    @classmethod
    def all_saved_messages(cls, user_id) -> List["Private_Message"]:
        with get_connection() as connection:
            messages = Database.get_my_saved_mail(connection, user_id)
            return [cls(message[3], message[4], message[5], message[6], message[0], message[1], message[2]) for message in messages]


    @classmethod
    def delete_message(cls, message_id):
        with get_connection() as connection:
            message = Private_Message.get_message_by_id(message_id)
            Database.delete_private_message(connection, message_id)