class GradeNotSelectedError(Exception):
    def __init__(self, message: str):
        self.message = message


class GradeNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidCommandError(Exception):
    def __init__(self, message: str):
        self.message = message
