from src.cloudidesandbox.exceptions.base import AppException


class TokenError(AppException):
    status_code = 401
    detail = "Something wrong with token"
    code = "TOKEN_ERROR"


class TokenExpiredError(TokenError):
    detail = "Token is expired"
    code = "TOKEN_EXPIRED"


class InvalidTokenError(TokenError):
    detail = "Token is invalid"
    code = "TOKEN_INVALID"
