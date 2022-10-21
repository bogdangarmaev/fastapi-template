from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Не найдено"):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail
