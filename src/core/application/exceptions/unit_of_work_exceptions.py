from src.kernel.application.application_exception import ApplicationException


class UnitOfWorkException(ApplicationException):
    pass


class UnitOfWorkNotInitializedError(UnitOfWorkException):
    """
    Raised on attempt to call unit of work methods outside context manager.
    """
    pass


class UnitOfWorkAlreadyInitializedError(UnitOfWorkException):
    """
    Raised on attempt to call context manager inside another context manager.
    A code example:

    async with unit_of_work() as initialized_uow:
        async with initialized_uow() as uow:  # here it raises error
            ...
    """
    pass


class UnitOfWorkAlreadyCompletedError(UnitOfWorkException):
    """
    Raised on attempt to call .commit or .rollback methods second time in one
    context manager.
    """
    pass
