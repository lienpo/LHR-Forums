from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

Private_Message = Tuple[int, datetime, bool, str, str, str, str]

CREATE_PRIVATE_MESSAGES = """CREATE TABLE IF NOT EXISTS private_messages (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, is_new BOOLEAN,
    subject TEXT, content TEXT, user_from TEXT, user_to TEXT,
    FOREIGN KEY(user_from) REFERENCES users(username),
    FOREIGN KEY(user_to) REFERENCES users(username)
);"""

INSERT_INTO_PRIVATE_MESSAGES = """INSERT INTO private_messages(origin, is_new, subject, content, user_from, user_to)
                               VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;"""

# -private_messages
SELECT_ALL_PRIVATE_MESSAGES = "SELECT * FROM private_messages;"
SELECT_MESSAGE_BY_ID = "SELECT * FROM private_messages WHERE id = %s;"
SELECT_MY_MAILBOX = "SELECT * FROM private_messages WHERE user_to = %s;"
HOW_MUCH_MAIL_I_HAVE = "SELECT COUNT(*) FROM private_messages WHERE user_to = %s;"
HOW_MUCH_NEW_MAIL_I_HAVE = "SELECT COUNT(*) FROM private_messages WHERE user_to = %s AND is_new = TRUE;"
SELECT_MESSAGES_I_SENT = "SELECT * FROM private_messages WHERE user_from = %s;"
SELECT_MY_NEW_MAIL = "SELECT * FROM private_messages WHERE user_to = %s AND is_new = TRUE;"
SELECT_MY_OLD_MAIL = "SELECT * FROM private_messages WHERE user_to = %s AND is_new = FALSE;"


MARK_MAIL_AS_SAVED = "UPDATE private_messages SET is_new = FALSE WHERE id = %s;"

DELETE_PRIVATE_MESSAGE = "DELETE FROM private_messages WHERE id = %s;"

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def create_private_message(connection, origin: datetime, is_new: bool, subject: str, content: str, user_from: str, user_to: str) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_PRIVATE_MESSAGES, (origin, is_new, subject, content, user_from, user_to))
        private_message_id = cursor.fetchone()[0]
        return private_message_id

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


def delete_private_message(connection, message_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_PRIVATE_MESSAGE, [message_id])

