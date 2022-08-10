from typing import Optional
from pydantic import BaseModel, validator


class ErrorResponse(BaseModel):
    error: bool = False
    errorMessage: Optional[str]

    @validator("errorMessage")
    def valid_page_number(cls, v, values):
        if values["error"] == True and len(v) < 1:
            raise ValueError("If error is set to true, error message cannot be empty")
        return v
