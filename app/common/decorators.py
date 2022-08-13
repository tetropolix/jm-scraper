from typing import Optional
from black import Any
from app.common.custom_classes import BaseModelDocumentable, DocumentedApp
from functools import wraps


def register_route(
    bp_or_app,
    rule: str,
    request: Optional[BaseModelDocumentable],
    response: Optional[BaseModelDocumentable],
    document: bool = True,
    **options: Any
):
    def decorator(function):
        if document:
            DocumentedApp.add_endpoint(
                endpoint=rule,
                request=request,
                response=response,
                description=function.__doc__,
            )
        function = bp_or_app.route(rule=rule, **options)(function)
        return function

    return decorator