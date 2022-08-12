from typing import List, Optional
from pydantic import BaseModel, validator


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
            return cls.instance


class BaseModelDocumentable(BaseModel):
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    @classmethod
    def generate_schema(cls):
        return cls.schema()


class DocumentedApp(SingletonClass):
    ENDPOINTS = {}

    @classmethod
    def add_endpoint(
        cls,
        endpoint: str,
        request: BaseModelDocumentable,
        response: BaseModelDocumentable,
        description: Optional[str] = None,
    ):
        cls.ENDPOINTS[endpoint] = {
            "request": request,
            "response": response,
            "description": description,
        }

    @classmethod
    def add_additional_info_for_endpoint(
        cls, endpoint: str, non_existing_endpoint_error=False, **kwargs
    ):
        existing_endpoint = cls.ENDPOINTS.get(endpoint) is not None
        if non_existing_endpoint_error and existing_endpoint is None:
            raise KeyError(endpoint)
        if existing_endpoint is None:
            return
        # parse kwargs for json serialization
        if "methods" in kwargs:
            cls.ENDPOINTS[endpoint].update({"methods": list(kwargs["methods"])})

    @classmethod
    def schema(cls) -> dict:
        schema_dict = {}
        for key, value in cls.ENDPOINTS.items():
            schema_dict[key] = value
            req = value.get("request")
            res = value.get("response")
            if req:
                schema_dict[key]["request"] = req.generate_schema()
            if res:
                schema_dict[key]["response"] = res.generate_schema()
        return schema_dict


class ErrorResponse(BaseModel):
    error: bool = False
    errorMessage: Optional[str]

    @validator("errorMessage")
    def valid_page_number(cls, v, values):
        if values["error"] == True and len(v) < 1:
            raise ValueError("If error is set to true, error message cannot be empty")
        return v
