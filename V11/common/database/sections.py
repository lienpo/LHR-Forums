from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

Section = Tuple[int, datetime, str, str, str]

CREATE_SECTIONS = """CREATE TABLE IF NOT EXISTS sections (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, 
    title TEXT UNIQUE, description TEXT, creator_name TEXT, 
    FOREIGN KEY(creator_name) REFERENCES users(username)
);"""

INSERT_INTO_SECTIONS = "INSERT INTO sections(origin, title, description, creator_name) VALUES(%s, %s, %s, %s) RETURNING id;"

SELECT_ALL_SECTIONS = "SELECT * FROM sections;"
SELECT_SECTION_BY_TITLE = "SELECT * FROM sections WHERE title = %s;"
SELECT_SECTION_BY_ID = "SELECT * FROM sections WHERE id = %s;"
CHECK_FOR_SECTION_TITLE = "SELECT COUNT(*) FROM sections where title = %s;"

EDIT_SECTION = "UPDATE sections SET title = %s, content = %s WHERE id = %s;"

DELETE_SECTION = "DELETE FROM sections WHERE id = %s;"

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def create_section(connection, origin: datetime, title: str, description: str, creator_name) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_SECTIONS, (origin, title, description, creator_name))
        section_id = cursor.fetchone()[0]
        return section_id

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

def update_section(connection, title: str, content: str, section_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_SECTION, (title, content, section_id))

def delete_section(connection, section_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_SECTION, [section_id])