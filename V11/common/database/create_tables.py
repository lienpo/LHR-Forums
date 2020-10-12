from contextlib import contextmanager

import common.database.users as Users
import common.database.sections as Sections
import common.database.topics as Topics
import common.database.posts as Posts
import common.database.private_messages as Private_Messages
import common.database.replies as Replies

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


# ___CREATE TABLES___
def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(Users.CREATE_USERS)
        cursor.execute(Sections.CREATE_SECTIONS)
        cursor.execute(Topics.CREATE_TOPICS)
        cursor.execute(Posts.CREATE_POSTS)
        cursor.execute(Private_Messages.CREATE_PRIVATE_MESSAGES)
        cursor.execute(Replies.CREATE_REPLIES)
