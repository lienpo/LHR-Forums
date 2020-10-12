from typing import List, Tuple, Dict
from datetime import datetime
from contextlib import contextmanager


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


Section = Tuple[int, datetime, str, str, str]

CREATE_SECTIONS = """CREATE TABLE IF NOT EXISTS sections (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, 
    title TEXT, description TEXT, creator_name TEXT, 
    FOREIGN KEY(creator_name) REFERENCES users(username)
);"""

INSERT_INTO_SECTIONS = "INSERT INTO sections(origin, title, description, creator_name) VALUES(%s, %s, %s, %s) RETURNING id;"

SELECT_ALL_SECTIONS = "SELECT * FROM sections;"
SELECT_SECTION_BY_TITLE = "SELECT * FROM sections WHERE title = %s;"
SELECT_SECTION_BY_ID = "SELECT * FROM sections WHERE id = %s;"
CHECK_FOR_SECTION_TITLE = "SELECT COUNT(*) FROM sections where title = %s;"


def create_section(connection, origin: datetime, title: str, description: str, creator_name: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_SECTIONS, (origin, title, description, creator_name))
        post_id = cursor.fetchone()[0]
        return post_id


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

