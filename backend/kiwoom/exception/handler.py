from fastapi import HTTPException


class handler(HTTPException):
    status: int
    detail: str

    def __init__(self,
                 status: int = 200,
                 detail: str = None,
                 ):
        self.status = status
        self.detail = detail

    def code(self, code, comment: str = None):

        if code == 400:
            if comment is None:
                comment = "content already exists"
            raise HTTPException(
                status_code=400,
                detail=comment,
            )
        elif code == 404:
            if comment is None:
                comment = "router not found"
            raise HTTPException(
                status_code=404,
                detail=comment,
            )


handler = handler()
