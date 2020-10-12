from contextlib import contextmanager
from typing import List, Tuple

User = Tuple[int, str, str, str]
Topic = Tuple[int, str, str, str]
Post = Tuple[int, str, str, str]



# ----- CREATE COMMANDS
CREATE_USERS = """CREATE TABLE IF NOT EXISTS users
(id SERIAL PRIMARY KEY, username TEXT, email TEXT, password TEXT);"""
CREATE_TOPICS = """CREATE TABLE IF NOT EXISTS topics
(id SERIAL PRIMARY KEY, title TEXT, content TEXT, owner TEXT,
 FOREIGN KEY(owner) REFERENCES users (username));"""
CREATE_POSTS = """CREATE TABLE IF NOT EXISTS posts
(id SERIAL PRIMARY KEY, content TEXT, topic_id INTEGER, owner TEXT,
FOREIGN KEY(topic_id) REFERENCES topics (id),
FOREIGN KEY(owner) REFERENCES users (id));"""



# ----- SELECT COMMANDS

# users
SELECT_ALL_USERS = "SELECT * FROM users;"
SELECT_NEWEST_USERS = """SELECT username FROM users
                        WHERE users.id = (
                        SELECT id FROM users ORDER BY id DESC LIMIT 10
                        );"""
SELECT_USER = "SELECT * FROM users WHERE username = %s;"
DOES_USER_EXIST = "SELECT COUNT(*) FROM users where username = %s and password = %s;"

# topics
SELECT_ALL_TOPICS = "SELECT * FROM topics;"
SELECT_MY_TOPICS = "SELECT * FROM topics where username = %s;"
SELECT_LATEST_POST_IN_TOPIC = """SELECT * FROM posts
                              WHERE posts.id = %s ORDER BY DESC LIMIT 1
                              );"""
SELECT_TOPIC_BY_NAME = "SELECT * FROM topics where title = %s;"
SELECT_TOPICS_WITH_NEWEST_POSTS = """SELECT title FROM topics
JOIN posts ON DISTINCT topics.id = posts.topic_id
WHERE posts.topic_id = (
SELECT id FROM polls ORDER BY id DESC LIMIT 10
);"""

# posts
SELECT_ALL_POSTS = "SELECT * FROM posts;"
SELECT_NEWEST_POSTS = """SELECT * FROM posts
                    WHERE posts.id = (
                    SELECT id FROM polls ORDER BY id DESC LIMIT 10
                    );"""
SELECT_POSTS_FROM_USER = "SELECT * FROM posts WHERE owner = %s;"
SELECT_POSTS_IN_TOPIC = "SELECT * FROM posts WHERE topic_name = %s;"
SELECT_POST_BY_ID = "SELECT * FROM posts WHERE id = %s);"

# ----- INSERT NEW COMMANDS
INSERT_USER = "INSERT INTO users (username, email, password);"
INSERT_TOPIC = "INSERT INTO topics (title, content, owner);"
INSERT_POST = "INSERT INTO posts (content, topic_id, owner);"



# ----- EDIT COMMANDS
EDIT_USER = """UPDATE users
             SET username = %s, email = %s, password = %s
             WHERE users.id = %s"""
EDIT_TOPIC = """UPDATE topics
            SET title = %s, content = %s
            WHERE topics.title = %s"""
EDIT_POST = """UPDATE posts
            SET content = %s
            WHERE posts.id = %s"""



@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

# -- create all tables --
def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_TOPICS)
        cursor.execute(CREATE_POSTS)

# -- users --
def create_user(connection, username: str, email: str, password: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_USER, (username, email, password))
        user_id = cursor.fetchone()[0]
        return user_id

def get_newest_users(connection) -> List[User]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_NEWEST_USERS)
        return cursor.fetchall()

def get_user(connection, username: str) -> User:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_USER, username)
        return cursor.fetchone()

def does_user_exist(connection, username: str, password: str) -> bool:
    with get_cursor(connection) as cursor:
        in_sql = cursor.execute(DOES_USER_EXIST, (username, password)).fetchone()
        in_int = int(in_sql)
        if in_int == 0:
            return False
        else:
            return True

def edit_user(connection, username: str, email: str, password: str, id: int) -> User:
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_USER, (username, email, password, id))
        return cursor.fetchone()

# -- topics --
def create_topic(connection, title: str, content: str, owner: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_TOPIC, (title, content, owner))
        topic_id = cursor.fetchone()[0]
        return topic_id

def select_all_topics(connection) -> List[Topic]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_TOPICS)
        return cursor.fetchall()

def get_topic_by_name(connection, title: str) -> Topic:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPIC_BY_NAME, title)
        return cursor.fetchone()


def select_users_topics(connection, username: str) -> List[Topic]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_MY_TOPICS, username)
        return cursor.fetchall()

def topics_with_newest_posts(connection) -> List[Topic]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPICS_WITH_NEWEST_POSTS)
        return cursor.fetchall()

def latest_post_in_topic(connection, id: int) -> Post:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_LATEST_POST_IN_TOPIC)
        return cursor.fetchone()

def edit_topic(connection, title: str, content: str, orig_title) -> Topic:
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_TOPIC, (title, content, orig_title))
        return cursor.fetchone()

# -- posts --
def create_post(connection, content: str, topic_id: int, owner:str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_POST, (content, topic_id, owner))
        post_id = cursor.fetchone()[0]
        return post_id


def newest_posts(connection) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_NEWEST_POSTS)
        return cursor.fetchall()


def posts_in_topic(connection, topic_name: str) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_IN_TOPIC, topic_name)
        return cursor.fetchall()


def get_post_by_id(connection, post_id: int) -> Post:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POST_BY_ID, post_id)
        return cursor.fetchall()


def posts_from_user(connection, owner: str) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_FROM_USER, owner)
        return cursor.fetchall()

def edit_post(connection, new_content, post_id: str):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_POST, (new_content, post_id))
        return cursor.fetchone()