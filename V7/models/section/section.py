import datetime
from typing import List

import common.database as Database
from common.connection_pool import get_connection
import models.section.errors as SectionErrors

class Section:
    def __init__(self, TITLE: str, DESCRIPTION: str, USER_ID: int, _ID: int = None, _ORIGIN: datetime = None):
        self.title = TITLE
        self.description = DESCRIPTION
        self.user_id = USER_ID
        self.origin = datetime.datetime.now() if _ORIGIN is None else _ORIGIN
        self.id = _ID

    def __repr__(self) -> str:
        return f"Section({self.id!r}, {self.origin!r}, {self.title!r}, {self.description!r}, {self.user_id!r})"

    def save(self):
        with get_connection() as connection:
            new_post_id = Database.create_section(connection, self.origin, self.title, self.description, self.user_id)
            self.id = new_post_id

    @classmethod
    def all(cls) -> List["Section"]:
        with get_connection() as connection:
            sections = Database.get_sections(connection)
            return [cls(section[2], section[3], section[4], section[0], section[1]) for section in sections]

    @classmethod
    def get_by_id(cls, _id: int) -> "Section":
        with get_connection() as connection:
            section = Database.get_section_by_id(connection, _id)
            return cls(section[2], section[3], section[4], section[0], section[1])

    @classmethod
    def get_by_title(cls, title) -> "Section":
        with get_connection() as connection:
            section = Database.get_section_by_title(connection, title)
            return cls(section[2], section[3], section[4], section[0], section[1])

    @classmethod
    def start_section(cls, title: str, description: str, creator_id: int) -> bool:
        if cls.does_section_exist(title):
            raise SectionErrors.SectionAlreadyCreated("A member with this username already exists.")
        else:
            section = Section(title, description, creator_id)
            section.save()
        return True

    @staticmethod
    def does_section_exist(title) -> bool:
        with get_connection() as connection:
            answer = Database.check_for_section_title(connection, title)
            return answer

