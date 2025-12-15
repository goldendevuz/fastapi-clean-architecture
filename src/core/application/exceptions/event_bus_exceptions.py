from src.kernel.application.application_exception import ApplicationException


class EventBusException(ApplicationException):
    pass


class EventBusAlreadyStartedError(EventBusException):
    """
    Raised on attempt to call .start method second time without closing.
    """
    pass


class EventBusAlreadyClosedError(EventBusException):
    """
    Raised on attempt to call .close method second time without starting.
    """
    pass


class EventBusNotStartedError(EventBusException):
    """
    Raised on attempt to use event bus before starting it.
    """
    pass