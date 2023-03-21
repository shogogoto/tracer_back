from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    # status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, msg: str):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=msg
        )


class SystemError(Exception):
    pass


class DBConnectionRefusedError(SystemError):
    pass
