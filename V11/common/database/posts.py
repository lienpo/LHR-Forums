from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

Post = Tuple[int, datetime, str, int, str]

CREATE_POSTS = """CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, content TEXT,
    topic_id INTEGER, creator_name TEXT,
    FOREIGN KEY(topic_id) REFERENCES topics(id),
    FOREIGN KEY(creator_name) REFERENCES users(username)
);"""

INSERT_INTO_POSTS = "INSERT INTO posts (origin, content, topic_id, creator_name) VALUES(%s, %s, %s, %s) RETURNING id;"

# -posts-
SELECT_ALL_POSTS = "SELECT * FROM posts;"
SELECT_POST_BY_ID = "SELECT * FROM posts WHERE id = %s;"
SELECT_POSTS_BY_TOPIC = "SELECT * FROM posts WHERE topic_id = %s;"
SELECT_POSTS_BY_CREATOR = "SELECT * FROM posts WHERE creator_name = %s;"
TEN_NEWEST_POSTS = "SELECT * FROM posts ORDER BY origin DESC LIMIT 10;"
REPLIES_IN_POST_COUNT = "SELECT COUNT(*) FROM replies WHERE post_id = %s;"


EDIT_POST = "UPDATE posts SET content = %s WHERE id = %s;"

DELETE_POST = "DELETE FROM posts WHERE id = %s;"

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def create_post(connection, origin: datetime, content: str, topic_id: int, creator_name: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_POSTS, (origin, content, topic_id, creator_name))
        post_id = cursor.fetchone()[0]
        return post_id

# -posts-
def get_posts(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POSTS)
        return cursor.fetchall()


def get_posts_by_id(connection, post_id: int) -> Post:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POST_BY_ID, [post_id])
        return cursor.fetchone()


def get_posts_by_topic(connection, topic_id: int) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_BY_TOPIC, [topic_id])
        return cursor.fetchall()


def get_posts_by_user(connection, creator_name: str) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_BY_CREATOR, [creator_name])
        return cursor.fetchall()


def ten_newest_posts(connection) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(TEN_NEWEST_POSTS)
        return cursor.fetchall()

def update_post(connection, content: str, post_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_POST, (content, post_id))

def delete_post(connection, post_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_POST, [post_id])


def post_has_replies(connection, post_id: int) -> bool:
    with get_cursor(connection) as cursor:
        cursor.execute(REPLIES_IN_POST_COUNT, [post_id])
        amount = cursor.fetchone()[0]
        if amount == 0:
            return False
        else:
            return True


def post_reply_count(connection, post_id) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(REPLIES_IN_POST_COUNT, [post_id])
        return cursor.fetchone()[0]