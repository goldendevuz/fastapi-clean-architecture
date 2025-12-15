from src.kernel.application.application_exception import ApplicationException


class RepositoryException(ApplicationException):
    pass


class NotFoundError(RepositoryException):
    """
    Raised on attempt to update or delete aggregate that does not exist.
    """
    pass


class ConflictError(RepositoryException):
    """
    Raised on attempt to create a new aggregate with unique credentials that
    already exists.
    """
    pass


class VersionMismatchError(RepositoryException):
    """
    Raised on attempt to update an aggregate, but its version is old.
    """
    pass
