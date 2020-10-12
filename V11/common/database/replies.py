from contextlib import contextmanager
from typing import List, Tuple, Dict
from datetime import datetime

Reply = Tuple[int, datetime, str, str, int]

CREATE_REPLIES = """CREATE TABLE IF NOT EXISTS replies (
    id SERIAL PRIMARY KEY, origin TIMESTAMP, content TEXT,
    creator_name TEXT, post_id INTEGER,
    FOREIGN KEY(creator_name) REFERENCES users(username),
    FOREIGN KEY(post_id) REFERENCES posts(id) 
);"""

INSERT_INTO_REPLIES = "INSERT INTO replies (origin, content, creator_name, post_id) VALUES (%s, %s, %s, %s) RETURNING id;"

# -replies
SELECT_ALL_REPLIES = "SELECT * FROM replies;"
SELECT_REPLIES_IN_POST = "SELECT * FROM replies WHERE post_id = %s;"


EDIT_REPLY = "UPDATE replies SET content = %s where id = %s;"

DELETE_REPLY = "DELETE FROM replies where id = %s;"

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

def create_reply(connection, origin: datetime, content: str, creator_name: str, post_id: int) -> int:
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_INTO_REPLIES, (origin, content, creator_name, post_id))
        reply_id = cursor.fetchone()[0]
        return reply_id

def all_replies(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_REPLIES)
        return cursor.fetchall()


def replies_in_post(connection, post_id: int) -> List[Reply]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_REPLIES_IN_POST, [post_id])
        return cursor.fetchall()







def update_reply(connection, content: str, reply_id):
    with get_cursor(connection) as cursor:
        cursor.execute(EDIT_REPLY, (content, reply_id))

def delete_reply(connection, reply_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(DELETE_REPLY, [reply_id])