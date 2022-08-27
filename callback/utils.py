from django.core.validators import RegexValidator

from fastapi.responses import JSONResponse


def name_regex():
    """
    Player model name validator
    """
    name_regex = RegexValidator(
        regex="[A-Fa-f0-9]+",
        message="The name must contain only numbers from 0-9 and only letters from a-f")
    return name_regex


def check_error_message(e):
    """
    Returns the status code 500 if the error is about a larger amount of data
    """
    return 500 if ("value has at most") in e.message_dict['name'][0] else 400


def get_400_response(message):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": message
        }
    )


def get_500_response(message):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": message
        }
    )
