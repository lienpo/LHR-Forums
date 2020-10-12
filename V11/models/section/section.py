import datetime
from typing import List

import common.database.sections as Database
from common.connection_pool import get_connection
import models.section.errors as SectionErrors
from models.user import User

class Section:
    def __init__(self, TITLE: str, DESCRIPTION: str, CREATOR_NAME: str, _ID: int = None, _ORIGIN: datetime = None):
        self.title = TITLE
        self.description = DESCRIPTION
        self.creator_name = CREATOR_NAME
        self.origin = datetime.datetime.now() if _ORIGIN is None else _ORIGIN
        self.id = _ID

    def __repr__(self) -> str:
        return f"Section({self.id!r}, {self.origin!r}, {self.title!r}, {self.description!r}, {self.creator_name!r})"

    def save(self):
        with get_connection() as connection:
            new_post_id = Database.create_section(connection, self.origin, self.title, self.description, self.creator_name)
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
    def start_section(cls, title: str, description: str, creator_name: str) -> bool:
        if cls.does_section_exist(title):
            raise SectionErrors.SectionAlreadyCreated("A member with this username already exists.")
        else:
            section = Section(title, description, creator_name)
            section.save()
        return True

    @staticmethod
    def does_section_exist(title) -> bool:
        with get_connection() as connection:
            answer = Database.check_for_section_title(connection, title)
            return answer

