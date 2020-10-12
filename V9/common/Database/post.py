from typing import List, Tuple, Dict
from datetime import datetime
from contextlib import contextmanager


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


Post = Tuple[int, datetime, int, str, int, str]
Reply = Tuple[int, datetime, str, str, int]

CREATE_POSTS = """CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, reply_count INTEGER,
    content TEXT, topic_id INTEGER, creator_name TEXT,
    FOREIGN KEY(topic_id) REFERENCES topics(id),
    FOREIGN KEY(creator_name) REFERENCES users(username)
);"""

INSERT_INTO_POSTS = "INSERT INTO posts (origin, reply_count, content, topic_id, creator_name)" \
                    " VALUES(%s, %s, %s, %s, %s) RETURNING id;"

# -posts-
SELECT_ALL_POSTS = "SELECT * FROM posts;"
SELECT_POST_BY_ID = "SELECT * FROM posts WHERE id = %s;"
SELECT_POSTS_BY_TOPIC = "SELECT * FROM posts WHERE topic_id = %s;"
SELECT_POSTS_BY_CREATOR = "SELECT * FROM posts WHERE creator_name = %s;"
TEN_NEWEST_POSTS = "SELECT * FROM posts ORDER BY origin DESC LIMIT 10;"
SELECT_REPLY_COUNT = "SELECT COUNT(*) AS total FROM replies WHERE post_id = %s;"
USERS_REPLYING_TO_POST = "SELECT DISTINCT user_id FROM replies WHERE post_id = %s;"
ARE_REPLIES_VISIBLE = "SELECT are_replies_visible WHERE post_id = %s;"
SHOW_POST_REPLIES = "UPDATE posts SET are_replies_visible = TRUE where id = %s;"
HIDE_POST_REPLIES = "UPDATE posts SET are_replies_visible = FALSE WHERE id = %s;"
SELECT_ALL_REPLIES_OF_POST = "SELECT * FROM replies WHERE post_id = %s;"

EDIT_POST = "UPDATE posts SET content = %s WHERE id = %s;"

DELETE_POST = "DELETE FROM posts WHERE id = %s;"


def create_post(connection, origin: datetime, reply_count: int, content: str, topic_id: int, creator_name: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_POSTS, (origin, reply_count, content, topic_id, creator_name))
        post_id = cursor.fetchone()[0]
        return post_id


# -posts-
def get_posts(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POSTS)
        return cursor.fetchall()


def get_replies_in_post(connection, post_id) -> List[Reply]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_REPLIES_OF_POST, [post_id])
        return cursor.fetchall()


def get_posts_by_id(connection, post_id: int) -> Post:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POST_BY_ID, [post_id])
        return cursor.fetchone()


def users_that_replied_to_post(connection, post_id) -> List[str]:
    with get_cursor(connection) as cursor:
        all_user_ids = cursor.execute(USERS_REPLYING_TO_POST, [post_id])
        return all_user_ids


def get_posts_in_topic(connection, topic_id: int) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_BY_TOPIC, [topic_id])
        return cursor.fetchall()


def get_posts_by_user(connection, username: str) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_BY_CREATOR, [username])
        return cursor.fetchall()


def ten_newest_posts(connection) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(TEN_NEWEST_POSTS)
        return cursor.fetchall()


def post_replies(connection, post_id):
    with get_cursor(connection) as cursor:
        replies = cursor.execute(SHOW_POST_REPLIES, [post_id])
        return replies


def are_replies_visible(connection, post_id: int) -> bool:
    with get_cursor(connection) as cursor:
        are_they = cursor.execute(ARE_REPLIES_VISIBLE, [post_id])
        return are_they


def has_replies(connection, post_id) -> bool:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_REPLY_COUNT, [post_id])
        count = cursor.fetchone()[0]
        if count == 0:
            return False
        else:
            return True


def hide_replies(connection, post_id):
    with get_cursor(connection) as cursor:
        cursor.execute(HIDE_POST_REPLIES, [post_id])


def reply_count(connection, post_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_REPLY_COUNT, [post_id])
        post_id = cursor.fetchone()[0]
        return post_id


def update_post(connection, content: str, reply_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_POST, (content, reply_id))


# ___DELETE TABLE COLUMNS___
def delete_post(connection, post_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_POST, [post_id])

