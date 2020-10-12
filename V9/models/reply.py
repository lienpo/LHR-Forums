from typing import List
import datetime

import common.Database.reply as Database
from common.connection_pool import get_connection
from models.user import User

# Reply = Tuple[int, datetime, str, int, int]
class Reply:
    def __init__(self, CONTENT: str, CREATOR_NAME: str, POST_ID: int, _ID: int = None, _ORIGIN: datetime = None):
        self.content = CONTENT
        self.creator_name = CREATOR_NAME
        self.post_id = POST_ID
        self.id = _ID
        self.origin = datetime.datetime.now() if _ORIGIN is None else _ORIGIN

    def __repr__(self) -> str:
        return f"Reply({self.id!r}, {self.origin!r}, {self.content!r}, {self.creator_name!r}, {self.post_id!r})"

    def save(self):
        with get_connection() as connection:
            new_reply_id = Database.create_reply(connection, self.origin, self.content, self.creator_name, self.post_id)
            self.id = new_reply_id

    @classmethod
    def all_replies(cls) -> List["Reply"]:
        with get_connection() as connection:
            replies = Database.get_replies(connection)
            return [cls(reply[2], reply[3], reply[4], reply[0], reply[1]) for reply in replies]


