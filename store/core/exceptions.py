class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:

        if message:
            self.message = message


class NotFoundException(BaseException):
    message = "Not Found"


class InsertException(Exception):
    """Erro ao tentar inserir produto no banco."""

    pass
