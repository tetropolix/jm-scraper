import json
from typing import Optional
from flask import Response
from sqlalchemy import desc


class BaseJSONResponse(Response):
    def __init__(self, status: int, message: str = None, **kwargs):
        self.default_mimetype = "application/json"
        self.response = json.dumps({"message": "" if message == None else message})
        return super().__init__(
            status=status,
            response=self.response,
            mimetype=self.default_mimetype,
            **kwargs
        )


class StatusCodeResponse(BaseJSONResponse):
    status_code_messages = {
        400: "BAD REQUEST",
        404: "NOT FOUND",
        500: "INTERNAL SERVER ERROR",
    }

    def __init__(self, status_code: int, custom_message: str = None, **kwargs):
        if not custom_message:
            custom_message = self.status_code_messages.get(status_code)
        return super().__init__(status=status_code, message=custom_message, **kwargs)
