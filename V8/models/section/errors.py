class SectionError(Exception):
    def __init__(self, message):
        self.message = message


class SectionAlreadyCreated(SectionError):
    pass