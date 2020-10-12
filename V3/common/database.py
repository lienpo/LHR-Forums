from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

User = Tuple[int, datetime, str, str, str]
Topic = Tuple[int, datetime, str, str, int]
Post = Tuple[int, datetime, str, int, int]


# ___ALL SQL COMMANDS___



# -TO CREATE TABLES-
CREATE_USERS = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, username TEXT,
    email TEXT, password TEXT
);"""
CREATE_TOPICS = """CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, title TEXT,
    content TEXT, user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);"""
CREATE_POSTS = """CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, content TEXT,
    topic_id INTEGER, user_id INTEGER,
    FOREIGN KEY(topic_id) REFERENCES topics(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);"""

# -TO INSERT INTO TABLES-
INSERT_INTO_USERS = "INSERT INTO users (origin, username, email, password) VALUES(%s, %s, %s ,%s) RETURNING id;"
INSERT_INTO_TOPICS = "INSERT INTO topics (origin, title, content, user_id) VALUES(%s, %s, %s, %s) RETURNING id;"
INSERT_INTO_POSTS = "INSERT INTO posts (origin, content, topic_id, user_id) VALUES(%s, %s, %s, %s) RETURNING id;"

# -TO QUERY THROUGH TABLES-

# -users-
SELECT_ALL_USERS = "SELECT * FROM users;"
SELECT_USER_BY_ID = "SELECT * FROM users WHERE id = %s;"
SELECT_USER_BY_USERNAME = "SELECT * FROM users WHERE username = %s;"
CHECK_FOR_USERNAME = "SELECT COUNT(*) FROM users WHERE username = %s;"
TEN_NEWEST_USERS = "SELECT * FROM users ORDER BY origin DESC LIMIT 10;"

# -topics-
SELECT_ALL_TOPICS = "SELECT * FROM topics;"
SELECT_TOPIC_BY_ID = "SELECT * FROM topics WHERE id = %s;"
SELECT_TOPIC_BY_TITLE = "SELECT * FROM topics WHERE title = %s;"
SELECT_TOPIC_BY_CREATOR = "SELECT * FROM topics WHERE user_id = %s;"
SELECT_ALL_USERS_POSTING = "SELECT * FROM users INNER JOIN posts "
CHECK_FOR_TOPIC_TITLE = "SELECT COUNT(*) FROM topics WHERE title = %s;"

# -posts-
SELECT_ALL_POSTS = "SELECT * FROM posts;"
SELECT_POST_BY_ID = "SELECT * FROM posts WHERE id = %s;"
SELECT_POSTS_BY_TOPIC = "SELECT * FROM posts WHERE topic_id = %s;"
SELECT_POSTS_BY_CREATOR = "SELECT * FROM posts WHERE user_id = %s;"
TEN_NEWEST_POSTS = "SELECT * FROM posts ORDER BY origin DESC LIMIT 10;"

# -TO UPDATE A COLUMN-
EDIT_USER_PROFILE = """UPDATE users
                    SET username = %s, email = %s, password = %s
                    WHERE id = %s"""
EDIT_TOPIC = """UPDATE topics
            SET topic = %s, content = %s
            WHERE id = %s"""
EDIT_POST = "UPDATE posts SET content = %s WHERE id = %s"

# -TO DELETE A COLUMN-
DELETE_USER = "DELETE FROM users WHERE id = %s"
DELETE_TOPIC = "DELETE FROM topics WHERE id = %s"
DELETE_POST = "DELETE FROM posts WHERE id = %s"


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


# ___CREATE TABLES___
def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_TOPICS)
        cursor.execute(CREATE_POSTS)


# ___ADD TO TABLES___
def create_user(connection, origin: datetime, username: str, email: str, password: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_USERS, (origin, username, email, password))
        user_id = cursor.fetchone()[0]
        return user_id


def create_topic(connection, origin: datetime, title: str, content: str, user_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_TOPICS, (origin, title, content, user_id))
        topic_id = cursor.fetchone()[0]
        return topic_id


def create_post(connection, origin: datetime, content: str, topic_id: int, user_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_POSTS, (origin, content, topic_id, user_id))
        post_id = cursor.fetchone()[0]
        return post_id


# ___QUERY(SEARCH) THROUGH TABLES___
# -users-
def get_users(connection) -> List[User]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_USERS)
        return cursor.fetchall()


def get_user_by_id(connection, user_id: int) -> User:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_USER_BY_ID, [user_id])
        return cursor.fetchone()


def get_user_by_username(connection, username: str) -> User:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_USER_BY_USERNAME, [username])
        return cursor.fetchone()


def check_for_username(connection, username: str) -> bool:
    with get_cursor(connection) as cursor:
        cursor.execute(CHECK_FOR_USERNAME, [username])
        amount = cursor.fetchone()[0]
        if amount == 0:
            return False
        else:
            return True


def ten_newest_users(connection) -> List[User]:
    with get_cursor(connection) as cursor:
        cursor.execute(TEN_NEWEST_USERS)
        return cursor.fetchall()


# -topics-
def get_topics(connection) -> List[Topic]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_TOPICS)
        return cursor.fetchall()


def get_topic_by_id(connection, topic_id: int) -> Topic:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPIC_BY_ID, [topic_id])
        return cursor.fetchone()


def get_topic_by_title(connection, topic_title: str) -> Topic:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPIC_BY_TITLE, [topic_title])
        return cursor.fetchone()


def get_topics_by_user(connection, user_id: int) -> List[Topic]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPIC_BY_CREATOR, [user_id])
        return cursor.fetchall()


def check_for_title(connection, title: str) -> bool:
    with get_cursor(connection) as cursor:
        cursor.execute(CHECK_FOR_TOPIC_TITLE, [title])
        amount = cursor.fetchone()[0]
        if amount == 0:
            return False
        else:
            return True


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


def get_posts_by_user(connection, user_id: int) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_BY_CREATOR, [user_id])
        return cursor.fetchall()


def ten_newest_posts(connection) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(TEN_NEWEST_POSTS)
        return cursor.fetchall()

# ___UPDATE TABLES WITH NEW VALUES___
def update_user(connection, username: str, email: str, password: str, user_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_USER_PROFILE, (username, email, password, user_id))


def update_topic(connection, title: str, content: str, topic_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_TOPIC, (title, content, topic_id))


def update_post(connection, content: str, post_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_POST, (content, post_id))


# ___DELETE TABLE COLUMNS___
def delete_user(connection, user_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_USER, [user_id])


def delete_topic(connection, topic_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_TOPIC, [topic_id])


def delete_post(connection, post_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_POST, [post_id])

