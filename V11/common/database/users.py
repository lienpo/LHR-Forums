from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

User = Tuple[int, datetime, str, str, str]

CREATE_USERS = """CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, username TEXT UNIQUE,
    email TEXT, password TEXT
);"""

INSERT_INTO_USERS = "INSERT INTO users (origin, username, email, password) VALUES(%s, %s, %s ,%s) RETURNING id;"

SELECT_ALL_USERS = "SELECT * FROM users;"
SELECT_USER_BY_ID = "SELECT * FROM users WHERE id = %s;"
SELECT_USER_BY_USERNAME = "SELECT * FROM users WHERE username = %s;"
CHECK_FOR_USERNAME = "SELECT COUNT(*) FROM users WHERE username = %s;"
TEN_NEWEST_USERS = "SELECT * FROM users ORDER BY origin DESC LIMIT 10;"
USERNAME_BY_ID = "SELECT username FROM users WHERE id = %s;"
HOW_MUCH_MAIL_I_HAVE = "SELECT COUNT(*) FROM private_messages WHERE user_to = %s;"
HOW_MUCH_NEW_MAIL_I_HAVE = "SELECT COUNT(*) FROM private_messages WHERE user_to = %s AND is_new = TRUE;"

EDIT_USER_PROFILE = """UPDATE users
                    SET username = %s, email = %s, password = %s
                    WHERE id = %s;"""

DELETE_USER = "DELETE FROM users WHERE id = %s;"

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def create_user(connection, origin: datetime, username: str, email: str, password: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_USERS, (origin, username, email, password))
        user_id = cursor.fetchone()[0]
        return user_id

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

def i_have_mail(connection, user_to: str) -> bool:
    with get_cursor(connection) as cursor:
        count = cursor.execute(HOW_MUCH_MAIL_I_HAVE, [user_to])
        if count == 0:
            return False
        else:
            return True


def i_have_new_mail(connection, user_to: str) -> bool:
    with get_cursor(connection) as cursor:
        count = cursor.execute(HOW_MUCH_NEW_MAIL_I_HAVE, [user_to])
        if count == 0:
            return False
        else:
            return True


def ten_newest_users(connection) -> List[User]:
    with get_cursor(connection) as cursor:
        cursor.execute(TEN_NEWEST_USERS)
        return cursor.fetchall()

def update_user(connection, username: str, email: str, password: str, user_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_USER_PROFILE, (username, email, password, user_id))

def delete_user(connection, user_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_USER, [user_id])