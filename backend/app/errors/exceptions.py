class AppError(Exception):
    """Base class for domain errors."""

    status_code = 500

    def __init__(self, message="Internal server error"):
        super().__init__(message)
        self.message = message


class ValidationError(AppError):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409
