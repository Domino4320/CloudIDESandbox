from src.cloudidesandbox.exceptions.base import AppException


class RedisNotInitializedError(AppException):

    detail = "redis is not initialized"
