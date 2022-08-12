from typing import Optional
from black import Any
from app.common.general_schemas import BaseModelDocumentable, DocumentedApp


def register_route(
    bp_or_app,
    rule: str,
    request: Optional[BaseModelDocumentable],
    response: Optional[BaseModelDocumentable],
    document: bool = True,
    **options: Any
):
    def decorator(func):
        if document:
            print("decorator", rule)
            DocumentedApp.add_endpoint(
                endpoint=rule,
                request=request,
                response=response,
                description=func.__doc__,
            )
        func = bp_or_app.route(rule=rule, **options)(func)
        return func

    return decorator
