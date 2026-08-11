class AppException(Exception):
    status_code: int = 500
    detail: str = "Internal server error"
    code: str = "INTERNAL_SERVER_ERROR"

    def __init__(
        self,
        status_code: int | None = None,
        detail: str | None = None,
        code: str | None = None,
    ):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail
        if code is not None:
            self.code = code

        super().__init__(self.detail)
