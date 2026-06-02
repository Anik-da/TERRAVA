from fastapi import HTTPException, status


class TerravaException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "INTERNAL_SERVER_ERROR"
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class CredentialsException(TerravaException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status_code.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="INVALID_CREDENTIALS"
        )


class PermissionDeniedException(TerravaException):
    def __init__(self, detail: str = "Permission denied for this resource"):
        super().__init__(
            status_code=status_code.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="PERMISSION_DENIED"
        )


class NotFoundException(TerravaException):
    def __init__(self, detail: str = "Requested resource not found"):
        super().__init__(
            status_code=status_code.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="RESOURCE_NOT_FOUND"
        )
