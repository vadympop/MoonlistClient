class MoonbotsException(BaseException):
    pass


class HTTPException(MoonbotsException):
    def __init__(self, json):
        self.json = json


class ClientException(MoonbotsException):
    pass


class Unauthorized(HTTPException):
    pass


class NotFound(HTTPException):
    pass


class Forbidden(HTTPException):
    pass


class BadRequest(HTTPException):
    pass


class ServerError(HTTPException):
    pass


class RateLimited(HTTPException):
    pass