from flask import render_template

from app.common.custom_responses import StatusCodeResponse


def handler_400(e):
    print(e)
    return StatusCodeResponse(400)
