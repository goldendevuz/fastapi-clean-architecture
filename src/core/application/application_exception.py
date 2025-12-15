

class ApplicationException(BaseException):

    def __init__(self, message: str, *args: object, **kwargs: object) -> None:
        super().__init__(message, *args, **kwargs)
        