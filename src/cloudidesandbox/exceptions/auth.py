from src.cloudidesandbox.exceptions.base import AppException


class BusyLoginError(AppException):
    code = "BUSY LOGIN"
    detail = "login is busy"
    status_code = 400
