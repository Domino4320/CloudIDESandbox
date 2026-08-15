from src.cloudidesandbox.exceptions.base import AppException


class BusyLoginError(AppException):
    code = "BUSY_LOGIN"
    detail = "login is busy"
    status_code = 409


class InvalidCredentialsError(AppException):
    code = "INVALID_CREDENTIALS"
    detail = "credentials are invalid"
    status_code = 401
