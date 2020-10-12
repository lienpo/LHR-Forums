from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

User = Tuple[int, datetime, str, str, str]
Topic = Tuple[int, datetime, str, str, str, int]
Post = Tuple[int, datetime, str, int, str]
Section = Tuple[int, datetime, str, str, str]
Private_Message = Tuple[int, datetime, bool, str, str, str, str]
Reply = Tuple[int, datetime, str, str, int]


# ___ALL SQL COMMANDS___



# -TO CREATE TABLES-

CREATE_USERS = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, username TEXT UNIQUE,
    email TEXT, password TEXT
);"""
CREATE_SECTIONS = """CREATE TABLE IF NOT EXISTS sections (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, 
    title TEXT, description TEXT, creator_name TEXT, 
    FOREIGN KEY(creator_name) REFERENCES users(username)
);"""
CREATE_PRIVATE_MESSAGES = """CREATE TABLE IF NOT EXISTS private_messages (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, is_new BOOLEAN,
    subject TEXT, content TEXT, user_from TEXT, user_to TEXT,
    FOREIGN KEY(user_from) REFERENCES users(username),
    FOREIGN KEY(user_to) REFERENCES users(username)
);"""
CREATE_TOPICS = """CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, title TEXT,
    content TEXT, creator_name TEXT, section_id INTEGER,
    FOREIGN KEY(creator_name) REFERENCES users(username),
    FOREIGN KEY(section_id) REFERENCES sections(id)
);"""
CREATE_POSTS = """CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, content TEXT,
    topic_id INTEGER, creator_name TEXT,
    FOREIGN KEY(topic_id) REFERENCES topics(id),
    FOREIGN KEY(creator_name) REFERENCES users(username)
);"""
CREATE_REPLIES = """CREATE TABLE IF NOT EXISTS replies (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, content TEXT,
    creator_name TEXT, post_id INTEGER,
    FOREIGN KEY(creator_name) REFERENCES users(username),
    FOREIGN KEY(post_id) REFERENCES posts(id) 
);"""

# -TO INSERT INTO TABLES-
INSERT_INTO_USERS = "INSERT INTO users (origin, username, email, password) VALUES(%s, %s, %s ,%s) RETURNING id;"
INSERT_INTO_TOPICS = "INSERT INTO topics (origin, title, content, creator_name, section_id) " \
                     "VALUES(%s, %s, %s, %s, %s) RETURNING id;"
INSERT_INTO_POSTS = "INSERT INTO posts (origin, content, topic_id, creator_name) VALUES(%s, %s, %s, %s) RETURNING id;"
INSERT_INTO_SECTIONS = "INSERT INTO sections(origin, title, description, creator_name) VALUES(%s, %s, %s, %s) RETURNING id;"
INSERT_INTO_PRIVATE_MESSAGES = """INSERT INTO private_messages(origin, is_new, subject, content, user_from, user_to)
                               VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;"""
INSERT_INTO_REPLIES = "INSERT INTO replies (origin, content, creator_name, post_id) VALUES (%s, %s, %s, %s) RETURNING id;"


# -TO QUERY THROUGH TABLES-
# -users-
SELECT_ALL_USERS = "SELECT * FROM users;"
SELECT_USER_BY_ID = "SELECT * FROM users WHERE id = %s;"
SELECT_USER_BY_USERNAME = "SELECT * FROM users WHERE username = %s;"
CHECK_FOR_USERNAME = "SELECT COUNT(*) FROM users WHERE username = %s;"
TEN_NEWEST_USERS = "SELECT * FROM users ORDER BY origin DESC LIMIT 10;"
USERNAME_BY_ID = "SELECT username FROM users WHERE id = %s;"

# -topics-
SELECT_ALL_TOPICS = "SELECT * FROM topics;"
SELECT_TOPIC_BY_ID = "SELECT * FROM topics WHERE id = %s;"
SELECT_TOPIC_BY_TITLE = "SELECT * FROM topics WHERE title = %s;"
SELECT_TOPIC_BY_CREATOR = "SELECT * FROM topics WHERE creator_name = %s;"
SELECT_ALL_USERS_POSTING = "SELECT * FROM users INNER JOIN posts "
CHECK_FOR_TOPIC_TITLE = "SELECT COUNT(*) FROM topics WHERE title = %s;"
SELECT_TOPICS_FOR_SECTION = "SELECT * FROM topics where section_id = %s;"

# -posts-
SELECT_ALL_POSTS = "SELECT * FROM posts;"
SELECT_POST_BY_ID = "SELECT * FROM posts WHERE id = %s;"
SELECT_POSTS_BY_TOPIC = "SELECT * FROM posts WHERE topic_id = %s;"
SELECT_POSTS_BY_CREATOR = "SELECT * FROM posts WHERE creator_name = %s;"
TEN_NEWEST_POSTS = "SELECT * FROM posts ORDER BY origin DESC LIMIT 10;"

# -sections
SELECT_ALL_SECTIONS = "SELECT * FROM sections;"
SELECT_SECTION_BY_TITLE = "SELECT * FROM sections WHERE title = %s;"
SELECT_SECTION_BY_ID = "SELECT * FROM sections WHERE id = %s;"
CHECK_FOR_SECTION_TITLE = "SELECT COUNT(*) FROM sections where title = %s;"

# -private_messages
SELECT_ALL_PRIVATE_MESSAGES = "SELECT * FROM private_messages;"
SELECT_MESSAGE_BY_ID = "SELECT * FROM private_messages WHERE id = %s;"
SELECT_MY_MAILBOX = "SELECT * FROM private_messages WHERE user_to = %s;"
HOW_MUCH_MAIL_I_HAVE = "SELECT COUNT(*) FROM private_messages WHERE user_to = %s;"
HOW_MUCH_NEW_MAIL_I_HAVE = "SELECT COUNT(*) FROM private_messages WHERE user_to = %s AND is_new = TRUE;"
SELECT_MESSAGES_I_SENT = "SELECT * FROM private_messages WHERE user_from = %s;"
SELECT_MY_NEW_MAIL = "SELECT * FROM private_messages WHERE user_to = %s AND is_new = TRUE;"
SELECT_MY_OLD_MAIL = "SELECT * FROM private_messages WHERE user_to = %s AND is_new = FALSE;"

# -replies
SELECT_ALL_REPLIES = "SELECT * FROM replies;"
SELECT_REPLIES_IN_POST = "SELECT * FROM replies WHERE post_id = %s;"
REPLIES_IN_POST_COUNT = "SELECT COUNT(*) FROM replies WHERE post_id = %s;"


# -TO UPDATE A COLUMN-
EDIT_USER_PROFILE = """UPDATE users
                    SET username = %s, email = %s, password = %s
                    WHERE id = %s;"""
EDIT_TOPIC = """UPDATE topics
            SET topic = %s, content = %s
            WHERE id = %s;"""
EDIT_POST = "UPDATE posts SET content = %s WHERE id = %s;"
MARK_MAIL_AS_SAVED = "UPDATE private_messages SET is_new = FALSE WHERE id = %s;"
EDIT_REPLY = "UPDATE replies SET content = %s where id = %s;"

# -TO DELETE A COLUMN-
DELETE_USER = "DELETE FROM users WHERE id = %s;"
DELETE_TOPIC = "DELETE FROM topics WHERE id = %s;"
DELETE_POST = "DELETE FROM posts WHERE id = %s;"
DELETE_PRIVATE_MESSAGE = "DELETE FROM private_messages WHERE id = %s;"
DELETE_REPLY = "DELETE FROM replies where id = %s;"

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


# ___CREATE TABLES___
def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_SECTIONS)
        cursor.execute(CREATE_TOPICS)
        cursor.execute(CREATE_POSTS)
        cursor.execute(CREATE_PRIVATE_MESSAGES)
        cursor.execute(CREATE_REPLIES)


# ___ADD TO TABLES___
def create_user(connection, origin: datetime, username: str, email: str, password: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_USERS, (origin, username, email, password))
        user_id = cursor.fetchone()[0]
        return user_id


def create_topic(connection, origin: datetime, title: str, content: str, creator_name: str, section_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_TOPICS, (origin, title, content, creator_name, section_id))
        topic_id = cursor.fetchone()[0]
        return topic_id


def create_post(connection, origin: datetime, content: str, topic_id: int, creator_name: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_POSTS, (origin, content, topic_id, creator_name))
        post_id = cursor.fetchone()[0]
        return post_id


def create_section(connection, origin: datetime, title: str, description: str, creator_name) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_SECTIONS, (origin, title, description, creator_name))
        section_id = cursor.fetchone()[0]
        return section_id


def create_private_message(connection, origin: datetime, is_new: bool, subject: str, content: str, user_from: str, user_to: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_PRIVATE_MESSAGES, (origin, is_new, subject, content, user_from, user_to))
        private_message_id = cursor.fetchone()[0]
        return private_message_id


def create_reply(connection, origin: datetime, content: str, creator_name: str, post_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_REPLIES, (origin, content, creator_name, post_id))
        reply_id = cursor.fetchone()[0]
        return reply_id


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


def get_topics_in_section(connection, section_id: int) -> List[Section]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPICS_FOR_SECTION, [section_id])
        return cursor.fetchall()


def get_topic_by_id(connection, topic_id: int) -> Topic:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPIC_BY_ID, [topic_id])
        return cursor.fetchone()


def get_topic_by_title(connection, topic_title: str) -> Topic:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPIC_BY_TITLE, [topic_title])
        return cursor.fetchone()


def get_topics_by_user(connection, creator_name) -> List[Topic]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TOPIC_BY_CREATOR, [creator_name])
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


def get_posts_by_user(connection, creator_name: str) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POSTS_BY_CREATOR, [creator_name])
        return cursor.fetchall()


def ten_newest_posts(connection) -> List[Post]:
    with get_cursor(connection) as cursor:
        cursor.execute(TEN_NEWEST_POSTS)
        return cursor.fetchall()

# - sections-
def get_sections(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_SECTIONS)
        return cursor.fetchall()


def get_section_by_id(connection, _id: int) -> Section:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_SECTION_BY_ID, [_id])
        return cursor.fetchone()


def get_section_by_title(connection, title) -> Section:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_SECTION_BY_TITLE, [title])
        return cursor.fetchone()


def check_for_section_title(connection, title: str) -> bool:
    with get_cursor(connection) as cursor:
        cursor.execute(CHECK_FOR_SECTION_TITLE, [title])
        amount = cursor.fetchone()[0]
        if amount == 0:
            return False
        else:
            return True


# - private_mails-
def get_private_messages(connection) -> List[Private_Message]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_PRIVATE_MESSAGES)
        return cursor.fetchall()


def get_my_mail(connection, user_to: str) -> List[Private_Message]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_MY_MAILBOX, [user_to])
        return cursor.fetchall()


def get_message_by_id(connection, message_id: int) -> Private_Message:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_MESSAGE_BY_ID, [message_id])
        return cursor.fetchone()


def get_my_new_mail(connection, user_to: str) -> List[Private_Message]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_MY_NEW_MAIL, [user_to])
        return cursor.fetchall()


def get_my_saved_mail(connection, user_to: str) -> List[Private_Message]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_MY_OLD_MAIL, [user_to])
        return cursor.fetchall()


def i_have_mail(connection, user_to: str) -> bool:
    with get_cursor(connection) as cursor:
        count = cursor.execute(HOW_MUCH_MAIL_I_HAVE, [user_to])
        if count == 0:
            return False
        else:
            return True


def username_by_id(connection, user_id: int) -> str:
    with get_cursor(connection) as cursor:
        name = cursor.execute(USERNAME_BY_ID, [user_id])
        return name.fetchone()[0]


def i_have_new_mail(connection, user_to: str) -> bool:
    with get_cursor(connection) as cursor:
        count = cursor.execute(HOW_MUCH_NEW_MAIL_I_HAVE, [user_to])
        if count == 0:
            return False
        else:
            return True


def set_as_saved(connection, private_message_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(MARK_MAIL_AS_SAVED, [private_message_id])


# - replies-
def all_replies(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_REPLIES)
        return cursor.fetchall()


def replies_in_post(connection, post_id: int) -> List[Reply]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_REPLIES_IN_POST, [post_id])
        return cursor.fetchall()


def post_reply_count(connection, post_id) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(REPLIES_IN_POST_COUNT, [post_id])
        return cursor.fetchone()[0]


def post_has_replies(connection, post_id: int) -> bool:
    with get_cursor(connection) as cursor:
        cursor.execute(REPLIES_IN_POST_COUNT, [post_id])
        amount = cursor.fetchone()[0]
        if amount == 0:
            return False
        else:
            return True


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

def update_reply(connection, content: str, reply_id):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_REPLY, (content, reply_id))

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


def delete_private_message(connection, message_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_PRIVATE_MESSAGE, [message_id])


def delete_reply(connection, reply_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_REPLY, [reply_id])
