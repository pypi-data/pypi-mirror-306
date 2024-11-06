class MindControlError(Exception):
    """Base class for exceptions in the MindControl API."""

    pass


class InvalidVersion(MindControlError, ValueError):
    """Exception raised when an invalid combination of version parameters is provided."""

    def __init__(self, message: str):
        super().__init__(message)
