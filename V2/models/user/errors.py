class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotFoundError(UserError):
    pass


class UserAlreadyRegistered(UserError):
    pass


class InvalidUsernameError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass