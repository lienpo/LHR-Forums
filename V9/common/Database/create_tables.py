from contextlib import contextmanager
import common.Database.user as user
import common.Database.section as section
import common.Database.private_message as private_message
import common.Database.topic as topic
import common.Database.post as post
import common.Database.reply as reply


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


# ___CREATE TABLES___
def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(user.CREATE_USERS)
        cursor.execute(section.CREATE_SECTIONS)
        cursor.execute(topic.CREATE_TOPICS)
        cursor.execute(post.CREATE_POSTS)
        cursor.execute(private_message.CREATE_PRIVATE_MESSAGES)
        cursor.execute(reply.CREATE_REPLIES)
