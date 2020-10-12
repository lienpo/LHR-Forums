from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

import common.database.sections as sections

Topic = Tuple[int, datetime, str, str, str, int]

CREATE_TOPICS = """CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, title TEXT UNIQUE,
    content TEXT, creator_name TEXT, section_id INTEGER,
    FOREIGN KEY(creator_name) REFERENCES users(username),
    FOREIGN KEY(section_id) REFERENCES sections(id)
);"""

INSERT_INTO_TOPICS = "INSERT INTO topics (origin, title, content, creator_name, section_id) " \
                     "VALUES(%s, %s, %s, %s, %s) RETURNING id;"

SELECT_ALL_TOPICS = "SELECT * FROM topics;"
SELECT_TOPIC_BY_ID = "SELECT * FROM topics WHERE id = %s;"
SELECT_TOPIC_BY_TITLE = "SELECT * FROM topics WHERE title = %s;"
SELECT_TOPIC_BY_CREATOR = "SELECT * FROM topics WHERE creator_name = %s;"
SELECT_ALL_USERS_POSTING = "SELECT * FROM users INNER JOIN posts "
CHECK_FOR_TOPIC_TITLE = "SELECT COUNT(*) FROM topics WHERE title = %s;"
SELECT_TOPICS_FOR_SECTION = "SELECT * FROM topics where section_id = %s;"

EDIT_TOPIC = """UPDATE topics
            SET topic = %s, content = %s
            WHERE id = %s;"""

DELETE_TOPIC = "DELETE FROM topics WHERE id = %s;"

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def create_topic(connection, origin: datetime, title: str, content: str, creator_name: str, section_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_TOPICS, (origin, title, content, creator_name, section_id))
        topic_id = cursor.fetchone()[0]
        return topic_id

def get_topics(connection) -> List[Topic]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_TOPICS)
        return cursor.fetchall()


def get_topics_in_section(connection, section_id: int) -> List[sections.Section]:
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

def update_topic(connection, title: str, content: str, topic_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_TOPIC, (title, content, topic_id))

def delete_topic(connection, topic_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_TOPIC, [topic_id])